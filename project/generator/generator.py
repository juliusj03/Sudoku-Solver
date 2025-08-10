"""This file contains everything needed to generate a new sudoku grid"""
import copy
import random
import sys
import time
from math import sqrt
from project.solver.solver import Solver
from project.Sudoku.Sudoku import Sudoku, Cell
from project.Hints.basis_matrix import Basis

class Generator(Solver):
    """
    self.generated is a variable containing the generated sudoku
    self.initial_values is used to populate an empty grid before generating.
    Difference in time finding solutions is due to the speed of the solver
    """

    def __init__(self, sudoku: Sudoku = Sudoku(), variant: str='standard', initial_values: int = 5) -> None:
        super().__init__(sudoku)
        variants = ['standard', 'diagonal', 'chess']
        self.generatedgrid = copy.deepcopy(sudoku.editablegrid)
        self.size = sudoku.size
        self.initial_values = initial_values
        self.variant = variant
        self.mode = variants.index(variant)
        self.previous_sol = None
        sys.setrecursionlimit(10000)

    def add_number_into_grid(self, sudoku: list[list[int]],
                             coordinates: None | tuple[int, int] = None) -> None:
        """adds a random number into the grid, at a random or specified location.
            It uses Basis.options() to reduce computational time."""
        bas = Basis(Sudoku(sudoku, self.size), self.variant)
        posnum = bas.options()
        posnum_len = [[len(x) for x in row] for row in posnum]
        if coordinates is None:
            # add number at the most useful location
            added = False
            while not added:
                y = random.randrange(0, self.size)
                x = random.choice(
                [i for i in range(len(posnum_len[y])) if posnum_len[y][i] == max(posnum_len[y])])
                if sudoku[y][x] == 0 and max(posnum_len[y]) > 1:
                    sudoku[y][x] = random.choice(posnum[y][x])
                    added = True
        else:
            # specified cell
            sudoku[coordinates[0]][coordinates[1]] = random.choice(
                            posnum[coordinates[0]][coordinates[1]])

    @staticmethod
    def compare_solutions(original: Sudoku, reversed_sud: Sudoku) -> tuple[
        bool, None | list[tuple[int, int]]]:
        """compares two solutions, returns wheter they are the same, if not
            it returns the coordinates of the cells that are different"""
        if original == reversed_sud:
            # use the sudoku __eq__ to see if they are the same solution
            return True, None
        # list all coordinates where the solutions differ
        sol_original = original.solutiongrid
        sol_reversed = reversed_sud.solutiongrid
        differences = []
        for row in range(original.size):
            for col in range(original.size):
                if sol_original[row][col] != sol_reversed[row][col]:
                    differences.append((row, col))
        return False, differences

    def create_starting_grid(self) -> None:
        """Fills the grid with the specified number of cells"""
        added_num = 0
        # first we fill the grid with the specified amount of numbers
        while added_num < self.initial_values:
            # we want to populate the top left box to make the solution seem more random
            if added_num < int(sqrt(self.size)) - 1:
                self.add_number_into_grid(self.generatedgrid, (random.randint(0, int(sqrt(self.size))), random.randint(0, int(sqrt(self.size))))) #type: ignore[arg-type]
            else:
                self.add_number_into_grid(self.generatedgrid) #type: ignore[arg-type]
            added_num += 1

    @staticmethod
    def flip_along_diagonal(sudoku: list[list[Cell]] | list[list[int]], diagonal_number = 1) -> list[list[Cell]] | list[list[int]]:
        """"Flips a sudoku along the chosen diagonal"""
        if diagonal_number == 2:
            sudoku = [row[::-1] for row in sudoku] #type: ignore[assignment]
        for i in range(len(sudoku)):
            for j in range(i, len(sudoku)):
                sudoku[i][j], sudoku[j][i] = sudoku[j][i], sudoku[i][j]  #type: ignore[assignment]
        if diagonal_number == 2:
            sudoku = [row[::-1] for row in sudoku] #type: ignore[assignment]
        return sudoku

    def solution_is_unique(self, sudoku_input: list[list[Cell]] | list[list[int]]) -> bool:
        """Checks if solution is the same if flipped several ways"""
        # we dont want to alter the input sudoku
        sudoku = copy.deepcopy(sudoku_input)
        flipped = sudoku[::-1]
        diagonal_grid_1 = self.flip_along_diagonal(copy.deepcopy(sudoku))
        diagonal_grid_2 = self.flip_along_diagonal(copy.deepcopy(sudoku), diagonal_number=2)

        # create the flipped sudokus
        sud_orignial = Sudoku(sudoku, self.size)
        sud_flipped = Sudoku(flipped, self.size)
        sud_diagonal_1 = Sudoku(diagonal_grid_1, self.size)
        sud_diagonal_2 = Sudoku(diagonal_grid_2, self.size)

        # solve them
        sol_original = Solver(sud_orignial, self.mode)
        sol_flipped = Solver(sud_flipped, self.mode)
        sol_original.solvebrute()
        sol_flipped.solvebrute()
        solution_1 = sud_orignial.solutiongrid
        solution_2 = sud_flipped.solutiongrid[::-1]

        # if this already fails we dont have to compute diagonals
        if solution_1 != solution_2:
            return False

        sol_diagonal_1 = Solver(sud_diagonal_1, self.mode)
        sol_diagonal_2 = Solver(sud_diagonal_2, self.mode)
        sol_diagonal_1.solvebrute()
        sol_diagonal_2.solvebrute()
        solution_3 = self.flip_along_diagonal(sud_diagonal_1.solutiongrid)
        solution_4 = self.flip_along_diagonal(sud_diagonal_2.solutiongrid, diagonal_number=2)

        return solution_1 == solution_2 == solution_3 == solution_4

    def generate_sudoku(self) -> list[list[Cell]] | list[list[int]]:
        """Compares the solution to the flipped solution and adds a number if they differ.
            The number is added in a cell where the answers differ to increase speed. 
            After 8 seconds it can take up to a minute to solve so after this time we stop
            the loop and find a solution using backwards removal."""
        self.create_starting_grid()
        # then we compute the solution and the solution of the flipped grid
        unique_solution = False
        starting_time = time.time()
        time_limit = 20

        while not unique_solution:
            # This segment finds the solutions of the original and the flipped grid
            # this is also the bottleneck when it comes to time
            flipped_grid = self.generatedgrid[::-1]
            sud_original = Sudoku(self.generatedgrid, self.size)
            sud_flipped = Sudoku(flipped_grid, self.size)
            sol_original = Solver(sud_original, self.mode)
            sol_flipped = Solver(sud_flipped, self.mode)
            sol_bool_1 = sol_original.solvebrute()
            # if sol_bool_1 took long we dont want to comput sol_bool_2
            if not time.time() < starting_time + time_limit:
                return self.backwards_removal(self.previous_sol) #type: ignore[arg-type]
            sol_bool_2 = sol_flipped.solvebrute()
            # compare the two solutions (flip the flipped grid back to the original orientation)
            comparison = self.compare_solutions(Sudoku(sud_original.solutiongrid, self.size),
                                                Sudoku(sud_flipped.solutiongrid[::-1], self.size))
            # if they are not the same, add a number in the original grid in a place
            # where the solutions differ

            if not comparison[0]:
                self.previous_sol = sud_original.solutiongrid #type: ignore[assignment]
                self.add_number_into_grid(self.generatedgrid, random.choice(comparison[1])) #type: ignore[arg-type]
            # if they are the same we must have a unique solution
            elif not (sol_bool_1 and sol_bool_2):
                return self.backwards_removal(self.previous_sol) #type: ignore[arg-type]
            else:
                unique_solution = self.solution_is_unique(self.generatedgrid)
                if not unique_solution:
                    return self.backwards_removal(self.previous_sol) #type: ignore[arg-type]
        return self.generatedgrid

    def quick_find_sudoku(self):
        """Method that immediately starts backtracking once a good starting
            grid is found. Much faster method useful for quick generation. """
        starting_grid_found = False
        while not starting_grid_found:
            self.create_starting_grid()
            sud_original = Sudoku(self.generatedgrid, size=self.size)
            sol_original = Solver(sud_original, self.mode)
            sol_bool_1 = sol_original.solvebrute()
            if sol_bool_1:
                starting_grid_found = True
                return self.backwards_removal(sud_original.solutiongrid)

    def backwards_removal(self, solution_grid: list[list[int]]) -> list[list[int]]:
        """Usually the generator creates an unsolvable sudoku, this function
            removes numbers from the solution of last solvable sudoku found,
            until it's solution is no longer unique at which point it returns
            the last unique sudoku"""
        if __name__ == '__main__':
            print('almost there')
        different = False
        while not different:
            prev_sol = copy.deepcopy(solution_grid)
            y = random.randrange(0, len(solution_grid))
            x = random.randrange(0, len(solution_grid))
            if solution_grid[y][x] != 0:
                solution_grid[y][x] = 0
                if not self.solution_is_unique(solution_grid):
                    different = True

        return prev_sol

