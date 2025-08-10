import sys
#imports sudoku and cell class from sudoku and sets recursion limit to higher than standard (1000)
sys.setrecursionlimit(50000)
from project.Sudoku.Sudoku import Sudoku, Cell
import math
import time
from project.Hints.basis_matrix import Basis


class Solver:
    """
    A class for solving Sudoku puzzles.

    ...

    Attributes:
    - sudoku (Sudoku): The Sudoku puzzle to solve.
    - mode (int): The mode of solving (default is 0).
    - iteration (int): The number of iterations during the solving process.
    - solutionbool (bool): Indicates whether a solution was found.
    """

    def __init__(self, sudoku: Sudoku, mode: int = 0) -> None:
        """
        Initializes a Sudoku solver.

        Parameters:
        - sudoku: Sudoku object to solve.
        - mode: Mode of solving (default is 0, 0 is for a standard sudoku so no special rules).
        """
        self.sudoku = sudoku
        self.basismode = 'standard'
        if mode == 1:
            self.basismode = 'diagonal'
        elif mode == 2:
            self.basismode = 'chess'
        basis = Basis(sudoku, self.basismode)
        basis.possibilities()
        self.mode = mode
        self.iteration = 0
        self.solutionbool = False
        self.blocksize = math.sqrt(self.sudoku.size)
    

    def solvebrute(self) -> bool:
        """
        Brute-force recursive method to solve the Sudoku. 
        This method is loosely based on https://medium.com/@ev.zafeiratos/sudoku-solver-with-python-a-methodical-approach-for-algorithm-optimization-part-1-b2c99887167f

        Returns:
        - True if the Sudoku is solved, False otherwise.
        """
        self.iteration += 1
        position = self.getcellpos()
        if position is None:
            self.solutionbool = True
            return True
        row, cell = position
        #for x in range(1, self.sudoku.size+1):
        for x in self.sudoku.editablegrid[row][cell].possiblenum:    
            if self.ruleset(position, x):
                # if row >  5:
                #     print(row, cell, x)
                self.sudoku.solutiongrid[row][cell] = Cell(x)
                if self.solvebrute():
                    return True
                self.sudoku.solutiongrid[row][cell] = Cell(0)
        self.solutionbool = False
        return False


    def getcellpos(self) -> tuple[int, int] | None:
        """
        Gets the position of the first empty cell in the Sudoku grid.

        Returns:
        - Tuple (row, cell) if an empty cell is found, None otherwise.
        """
        for row in range(self.sudoku.size):
            for cell in range(self.sudoku.size):
                if self.sudoku.solutiongrid[row][cell] == 0:
                    return row,cell
        return None
    

    def ruleset(self, position: tuple[int, int], x: int) -> bool:
        """
        Determines if a number x can be placed at a given position based on Sudoku rules.
        This support multiple rulesets so different rules can be used based on what the user wants
        Parameters:
        - position: Tuple (row, cell) representing the position in the Sudoku grid.
        - x: Number to check.

        Returns:
        - True if x can be placed at the given position, False otherwise.
        """
        row, cell = position
        if self.mode == 0:
            return all([self.colcheck(row, cell, x), self.rowcheck(row, cell, x), self.blockcheck(row, cell, x)])
        if self.mode == 1:
            return all([self.colcheck(row, cell, x), self.rowcheck(row, cell, x), self.blockcheck(row, cell, x), self.diagonalcheck(row, cell, x)])
        if self.mode == 2:
            return all([self.colcheck(row, cell, x), self.rowcheck(row, cell, x), self.blockcheck(row, cell, x), self.chesscheck(row, cell, x)])
        return False


    def colcheck(self, row: int, cell: int, num: int) -> bool:
        """
        Checks if a number can be placed in the column of the given position.

        Parameters:
        - row: Row index.
        - cell: Column index.
        - num: Number to check.

        Returns:
        - True if num can be placed in the column, False otherwise.
        """
        for y in range(self.sudoku.size):
            if self.sudoku.solutiongrid[y][cell] == num and y != row: 
                return False
        return True


    def rowcheck(self, row: int, cell: int, num: int) -> bool:
        """
        Checks if a number can be placed in the row of the given position.

        Parameters:
        - row: Row index.
        - cell: Column index.
        - num: Number to check.

        Returns:
        - True if num can be placed in the row, False otherwise.
        """
        for x in range(self.sudoku.size):
            if self.sudoku.solutiongrid[row][x] == num and x != cell:
                return False
        return True
    

    def diagonalcheck(self, row: int, cell: int, num: int) -> bool:
        """
        Checks if a number can be placed in the diagonals of the given position.

        Parameters:
        - row: Row index.
        - cell: Column index.
        - num: Number to check.

        Returns:
        - True if num can be placed in the diagonals, False otherwise.
        """
        if row == cell:
            for x in range(self.sudoku.size):
                if self.sudoku.solutiongrid[x][x] == num and x != cell:
                    return False
        if (self.sudoku.size - 1) == (row+cell):
            for x in range(self.sudoku.size):
                if self.sudoku.solutiongrid[x][self.sudoku.size-1-x] == num and x != row:
                    return False
        return True


    def blockcheck(self, row: int, cell: int, num: int) -> bool:
        """
        Checks if a number can be placed in the block of size squareroot(size) of the given position.

        Parameters:
        - row: Row index.
        - cell: Column index.
        - num: Number to check.

        Returns:
        - True if num can be placed in the block, False otherwise.
        """
        rowstart, rowend = int(self.blocksize * (row // self.blocksize)), int(self.blocksize + self.blocksize * (row // self.blocksize))
        cellstart, cellend = int(self.blocksize * (cell // self.blocksize)), int(self.blocksize + self.blocksize * (cell // self.blocksize))
        for y in range(rowstart, rowend):
            for x in range(cellstart, cellend):       
                if self.sudoku.solutiongrid[y][x] == num and (y, x) != (row, cell):
                    return False
        return True
    
    
    def chesscheck(self, row: int, cell: int, num: int) -> bool:
        """
        Checks if a number can be placed by checking if the same number is not a chess knights move away of the given position.

        Parameters:
        - row: Row index.
        - cell: Column index.
        - num: Number to check.

        Returns:
        - True if num can be is not in a knight move nearby, False otherwise.
        """
        possiblepositions = [(2,1), (1,2), (-1,2), (-2,1), (-2,-1), (-1,-2), (1,-2), (2,-1)]
        for pos in possiblepositions:
            ypos, xpos = row + pos[0], cell + pos[1]
            if ypos >= 0 and ypos <= self.sudoku.size - 1 and xpos >= 0 and xpos <= self.sudoku.size - 1:
                if self.sudoku.solutiongrid[ypos][xpos] == num:
                    return False
        return True


# sud = Sudoku(
#     [
#     [5, 3, 0, 0, 7, 0, 0, 0, 0],
#     [6, 0, 0, 1, 9, 5, 0, 0, 0],
#     [0, 9, 8, 0, 0, 0, 0, 6, 0],
#     [8, 0, 0, 0, 6, 0, 0, 0, 3],
#     [4, 0, 0, 8, 0, 3, 0, 0, 1],
#     [7, 0, 0, 0, 2, 0, 0, 0, 6],
#     [0, 6, 0, 0, 0, 0, 2, 8, 0],
#     [0, 0, 0, 4, 1, 9, 0, 0, 5],
#     [0, 0, 0, 0, 8, 0, 0, 7, 9]
# ])

# sud1 = Sudoku(    
#  [
#     [0, 2, 0, 5, 9, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 7, 0, 0, 0],
#     [9, 0, 0, 2, 0, 4, 8, 7, 1],
#     [0, 0, 0, 0, 8, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 2, 0, 0, 0, 0],
#     [6, 3, 7, 9, 0, 5, 0, 0, 8],
#     [0, 0, 0, 3, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 6, 1, 0, 3, 0]
# ])
# sud2 = Sudoku(    
#  [
#     [0, 0, 0, 0, 1, 0, 0, 0, 0],
#     [0, 0, 0, 3, 0, 2, 0, 0, 0],
#     [0, 0, 9, 0, 0, 0, 3, 0, 0],
#     [0, 2, 0, 0, 0, 0, 0, 4, 0],
#     [3, 0, 0, 0, 0, 0, 0, 0, 5],
#     [0, 4, 0, 0, 0, 0, 0, 6, 0],
#     [0, 0, 4, 0, 0, 0, 7, 0, 0],
#     [0, 0, 0, 1, 0, 8, 0, 0, 0],
#     [0, 0, 0, 0, 9, 0, 0, 0, 0]
# ])
# sud3 = Sudoku([
#  [12, 0, 0, 0, 11, 0, 14, 9, 6, 0, 0, 0, 2, 0, 0, 10],
#  [14, 1, 16, 0, 0, 13, 3, 0, 12, 0, 11, 0, 0, 7, 0, 9],
#  [0, 0, 0, 0, 16, 15, 0, 0, 0, 13, 1, 9, 12, 14, 0, 0],
#  [0, 0, 0, 10, 0, 2, 7, 0, 4, 0, 15, 8, 5, 0, 0, 16],
#  [0, 15, 0, 0, 0, 5, 13, 0, 10, 4, 16, 0, 0, 2, 0, 1],
#  [0, 7, 0, 0, 4, 0, 2, 3, 11, 8, 9, 0, 0, 0, 10, 0],
#  [0, 13, 0, 0, 6, 0, 0, 0, 0, 0, 14, 0, 9, 4, 12, 7],
#  [4, 8, 1, 3, 0, 0, 0, 16, 0, 2, 0, 13, 14, 0, 0, 5],
#  [0, 0, 0, 0, 0, 12, 0, 0, 9, 11, 0, 0, 7, 16, 8, 0],
#  [6, 10, 0, 2, 13, 7, 0, 0, 8, 16, 0, 0, 0, 0, 0, 11],
#  [0, 0, 9, 12, 3, 16, 0, 0, 0, 0, 0, 0, 0, 5, 4, 0],
#  [15, 0, 5, 7, 8, 0, 9, 0, 0, 0, 0, 0, 3, 0, 0, 6],
#  [0, 5, 10, 1, 0, 8, 11, 7, 0, 0, 3, 14, 0, 0, 16, 12],
#  [3, 0, 0, 0, 10, 6, 16, 0, 7, 1, 2, 12, 0, 0, 0, 0],
#  [13, 0, 0, 0, 9, 0, 12, 5, 16, 0, 0, 11, 1, 0, 2, 0],
#  [0, 0, 4, 0, 0, 3, 1, 13, 0, 6, 8, 0, 0, 15, 7, 0]
# ], 16)


# start = time.time()


# solv = Solver(sud2,2)
# solv.solvebrute()
# end = time.time()
# print(end - start)

# print(sud2.printsolution()) 