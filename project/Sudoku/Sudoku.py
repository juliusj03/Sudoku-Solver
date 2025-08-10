from __future__ import annotations
import math
import copy


class Sudoku:
    """
    A class representing a Sudoku puzzle.

    Attributes:
    - size (int): The size of the Sudoku grid (default is 9).
    - blockwidth (int): The width of each block in the Sudoku grid.
    - emptygrid (list[list[Cell]]): An empty Sudoku grid filled with Cell objects.
    - _originalgrid (list[list[Cell]]): The original Sudoku grid before any modifications.
    - editablegrid (list[list[Cell]]): The Sudoku grid that can be modified by the user.
    - solutiongrid (list[list[Cell]]): The solution to the Sudoku puzzle.
    """
    def __init__(self, sudoku: list[list[Cell]] | list[list[int]] | None = None, size: int = 9) -> None:
        """
        Initializes a Sudoku object.

        Parameters:
        - sudoku: Initial Sudoku configuration (list of lists of Cells or integers) or None to create an empty Sudoku.
        - size: Size of the Sudoku grid (default is 9).
        """
        self.size = size
        self.blockwidth = int(math.sqrt(size))
        self.emptygrid = self.fillgrid()
        self._originalgrid = copy.deepcopy(self.emptygrid)
        self.solutiongrid = copy.deepcopy(self.emptygrid)
        if sudoku is None:
            self.editablegrid = copy.deepcopy(self.emptygrid)
        else:
            self.originalgrid = sudoku


    def fillgrid(self) -> list[list[Cell]]:
        """
        Creates an empty Sudoku grid filled with Cell objects.

        Returns:
        - emptygrid: Empty Sudoku grid.
        """
        emptygrid = [[Cell(0) for x in range(self.size)] for y in range(self.size)]
        return emptygrid


    @property
    def originalgrid(self) -> list[list[Cell]] | list[list[int]]:
        """
        Getter for the originalgrid property.
        """
        return self._originalgrid
    

    @originalgrid.setter
    def originalgrid(self, grid: list[list[Cell]] | list[list[int]]) -> None:
        """
        Setter for the originalgrid property. Converts a grid of integers to a grid of Cell objects or if its already a grid cells it uses the cells.

        Parameters:
        - grid: New original Sudoku grid.
        """
        if isinstance(grid[0][0], int):
            for row in range(self.size):
                for col in range(self.size):
                    self.fillcoor(grid[row][col], row, col)
        else:
            self._originalgrid = [[Cell(val) if isinstance(val, int) else val for val in row] for row in grid]
        self.editablegrid = copy.deepcopy(self._originalgrid)
        self.solutiongrid = copy.deepcopy(self._originalgrid)       


    def fillcoor(self, num: Cell | int, row: int, col: int) -> None:
        """
        Fills a specific coordinate in the Sudoku grid. Used by the originalgrid setter

        Parameters:
        - num: Cell object or integer value to be placed in the grid.
        - row: Row index.
        - col: Column index.
        """
        if isinstance(num, int):
            self._originalgrid[row][col] = Cell(num)
            self.solutiongrid[row][col] = Cell(num)
        else:
            self.solutiongrid[row][col] = num
            self._originalgrid[row][col] = num


    def fillcooruser(self, num: int, row: int, col: int) -> None:
        """
        Fills a specific coordinate in the editable grid (user input).

        Parameters:
        - num: Integer value to be placed in the grid.
        - row: Row index.
        - col: Column index.
        """
        self.editablegrid[row][col] = Cell(num)


    def __repr__(self) -> str:
        """
        Returns a standard string representation of the Sudoku grid.
        """
        empstr = f"{'-'*self.size*int(math.sqrt(self.size))}\n"
        for y in range(self.size):
            for x in range(self.size):
                empstr += f" {self.editablegrid[y][x] }"
                if (x + 1) % self.blockwidth == 0 and (x + 1) != self.size:
                    empstr += " |"
            empstr += "\n"
            if (y + 1) % self.blockwidth == 0 and (y + 1) != self.size:
                empstr += f"{'-'*self.size*int(math.sqrt(self.size))}\n"
        empstr += f"{'-'*self.size*int(math.sqrt(self.size))}\n"
        return empstr


    def comparetoanswer(self) -> tuple[bool, int, int]:
        """
        Compares the editable grid to the solution grid to check for correctness.

        Returns:
        - Tuple (bool, row, col):
          - bool: True if the grids match, False otherwise.
          - row: Row index of the first incorrect cell.
          - col: Column index of the first incorrect cell.
        """
        for row in range(self.size):
            for col in range(self.size):
                if (
                    self.editablegrid[row][col] != self.solutiongrid[row][col]
                    and self.editablegrid[row][col] != 0
                ):
                    self.printsolution()
                    return False, row, col
        return True, 0, 0


    def printsolution(self) -> str:
        """
        Returns a string representation of the solution grid.

        Returns:
        - String representation of the solution grid.
        """
        empstr = f"{'-'*self.size*int(math.sqrt(self.size))}\n"
        for y in range(self.size):
            for x in range(self.size):
                empstr += f" {self.solutiongrid[y][x] }"
                if (x + 1) % self.blockwidth == 0 and (x + 1) != self.size:
                    empstr += " |"
            empstr += "\n"
            if (y + 1) % self.blockwidth == 0 and (y + 1) != self.size:
                empstr += f"{'-'*self.size*int(math.sqrt(self.size))}\n"
        empstr += f"{'-'*self.size*int(math.sqrt(self.size))}\n"
        return empstr


    def __eq__(self, other):
        """
        Overrides the equality comparison for Sudoku objects.

        Parameters:
        - other: Sudoku object or list to compare.

        Returns:
        - True if equal, False otherwise.
        """
        if isinstance(other, Sudoku):
            return self.originalgrid == other.originalgrid
        elif isinstance(other, list):
            othersud = Sudoku()
            othersud.originalgrid = other
            return self.originalgrid == othersud.originalgrid
        else:
            return False


class Cell:
    def __init__(self, defaultval: int = 0):
        """
        Initializes a Cell object.

        Parameters:
        - defaultval: Default value for the cell (default is 0, 0 is used as a not filled in sudoku cell).
        """
        self.possiblenum: list[int] = []
        self.notes = ['dummy', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ']
        self._value = defaultval


    @property
    def value(self) -> int:
        """
        Getter for the value property.
        """
        return self._value


    @value.setter
    def value(self, num: int) -> None:
        """
        Setter for the value property.
        """
        self._value = num


    def remove(self, num: int) -> None:
        """
        Removes a possible number from the list of possible numbers for the cell.

        Parameters:
        - num: Number to be removed.
        """
        if num in self.possiblenum:
            self.possiblenum.remove(num)


    def __repr__(self) -> str:
        """
        Returns a string representation of the Cell object.
        """
        return str(self.value)


    def __eq__(self, other: int | object) -> bool:
        """
        Overrides the equality comparison for Cell objects.

        Parameters:
        - other: Integer or Cell object to compare.

        Returns:
        - True if equal, False otherwise.
        
        Raises:
        - ValueError: If the 'other' parameter is neither an integer nor a Cell object.
        """
        if isinstance(other, int):
            return self.value == other
        elif isinstance(other, Cell):
            return self.value == other.value
        else:
            raise ValueError

    def clearnotes(self):
        self.notes = ['dummy', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ']



