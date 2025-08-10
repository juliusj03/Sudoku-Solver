import math
from typing import List
from project.Sudoku.Sudoku import Sudoku, Cell


class Basis:
    """
    A class representing the possibilities in a sudoku puzzle.
    It uses the Sudoku class to work with.

    Attributes:
    - size (int): The size of the Sudoku grid (default is 9).
    - blockwidth (int): The width of each block in the Sudoku grid.
    - emptygrid (list[list[Cell]]): An empty Sudoku grid filled with Cell objects.
    - number (list[int]): A list with number from 1 to size of sudoku to describe
                          all possible values
    """
    def __init__(self, sudoku: Sudoku, variant: str = 'standard') -> None:
        """
        Initializes a Basis object.

        Parameters:
        - sudoku: Initial Sudoku configuration (list of lists of Cells or integers)
                    or None to create an empty Sudoku.
        - variant: The variant (standard, diagonal, chess) of the sudoku passed.
        """
        self.sudoku = sudoku
        self.size = self.sudoku.size
        self.blockwidth = int(math.sqrt(self.size))
        self.numbers = list(range(1, self.size + 1))
        self.variant = variant

    # helper functions
    @staticmethod
    def check_type(lst: list) -> bool:
        """
        Checks whether a list consists of lists with integers or if it
        consists of lists with lists of integers.

        Parameters:
        - lst: a list
        Returns:
        - bool: False if it is an integer in a list in a list, True otherwise.
        """
        for item in lst:
            for subitem in item:
                if isinstance(subitem, list):
                    for sub_sub in subitem:
                        if isinstance(sub_sub, int):
                            return True
        return False

    @staticmethod
    def sud_to_values(sudoku: Sudoku) -> list[list[int]]:
        """
        Creates a list of the values in the sudoku.

        Parameters:
        - sudoku: a Sudoku class object
        Returns:
        - list[list[int]]: sudoku values in a list
        """
        return [[y.value for y in x] for x in sudoku.editablegrid]

    @staticmethod
    def sud_to_posnum(sudoku: Sudoku) -> list[list[list[int]]]:
        """
        Creates a list of the possible values in the sudoku.

        Parameters:
        - sudoku: a Sudoku class object
        Returns:
        - list[list[list[int]]]: sudoku possible values in a list
        """
        return [[y.possiblenum for y in x] for x in sudoku.editablegrid]

    def get_diagonal(self, row: int, column: int) -> List[Cell]:
        """
        Gets the numbers in the diagonal of the cell

        Parameters:
        - row: Row index.
        - cell: Column index.

        Returns:
        - list[int] with values that are in the diagonal and need to
        be removed from possiblenum.
        """
        numbers = []
        if row == column:
            for x in range(self.sudoku.size):
                if self.sudoku.editablegrid[x][x] != 0:
                    numbers.append(self.sudoku.editablegrid[x][x])
        if (self.sudoku.size - 1) == (row + column):
            for x in range(self.sudoku.size):
                if (self.sudoku.editablegrid[x][self.sudoku.size - 1 - x] != 0 and
                        self.sudoku.editablegrid[x][self.sudoku.size - 1 - x] not in numbers):
                    numbers.append(self.sudoku.editablegrid[x][self.sudoku.size - 1 - x])
        return numbers

    def get_chess(self, row: int, column: int) -> List[Cell]:
        """
        Gets the numbers in the chess options of the cell

        Parameters:
        - row: Row index.
        - cell: Column index.

        Returns:
        - list[int] with values that are in knight position of the cell
        and need to be removed from possiblenum.
        """
        possiblepositions = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1),
                             (-1, -2), (1, -2), (2, -1)]
        numbers = []
        for pos in possiblepositions:
            ypos, xpos = row + pos[0], column + pos[1]
            if (0 <= ypos < self.sudoku.size and 0 <= xpos < self.sudoku.size
                    and self.sudoku.editablegrid[ypos][xpos] != 0):
                numbers.append(self.sudoku.editablegrid[ypos][xpos])
        return numbers

    def row_to_columns(self, sudoku: Sudoku) -> Sudoku:
        """
        Creates a sudoko grid where the values of 1 column are put in a single list,
        so it transforms the rows into
        columns.

        Parameters:
        - sudoku: a Sudoku class object
        Returns:
        - new_sudoku: a Sudoku class object that has columns for rows in
        comparison to the input sudoku
        """
        new_sudoku = Sudoku(None, self.sudoku.size)
        for row in range(self.size):
            for col in range(self.size):
                new_sudoku.editablegrid[col][row].value = sudoku.editablegrid[row][col].value
                new_sudoku.editablegrid[col][row].possiblenum = (
                    sudoku.editablegrid[row][col].possiblenum)
        return new_sudoku

    def row_to_blocks(self, sudoku: Sudoku) -> Sudoku:
        """
        Creates a sudoko grid where the values of 1 block are put in a single list,
        so it transforms the rows into
        blocks.

        Parameters:
        - sudoku: a Sudoku class object
        Returns:
        - new_sudoku: a Sudoku class object that has blocks for rows
        in comparison to the input sudoku, the order is from top to bottom
        and then to the right, so in some cases it needs to be sorted later on.
        """
        values = self.sud_to_values(sudoku)
        posnums = self.sud_to_posnum(sudoku)
        new_sudoku = []

        for row_start in range(0, sudoku.size, self.blockwidth):
            for col_start in range(0, sudoku.size, self.blockwidth):
                block_values = []
                for i in range(self.blockwidth):
                    block_values.extend(values[row_start + i]
                                        [col_start: col_start + self.blockwidth])
                new_sudoku.append(block_values)

        sudok = Sudoku(None, self.size)
        sudok.originalgrid = new_sudoku

        if self.check_type(posnums):
            new_posnums = []
            for row_start in range(0, self.size, self.blockwidth):
                for col_start in range(0, self.size, self.blockwidth):
                    block_posnums = []
                    for i in range(self.blockwidth):
                        block_posnums.extend(posnums[row_start + i]
                                             [col_start: col_start + self.blockwidth])
                    new_posnums.append(block_posnums)

            for row, row_posnum in enumerate(new_posnums):
                for col, cell_posnum in enumerate(row_posnum):
                    sudok.editablegrid[row][col].possiblenum = cell_posnum
        return sudok

    def all_options(self, sudoku: Sudoku) -> Sudoku:
        """
        Creates a Sudoko grid where the 0 values are replaced by [1 to size].
        To get all possible values that can go there.

        Parameters:
        - sudoku: a Sudoku  object

        Returns:
        - sudoku: it changes the Sudoku object that has been inputted
        so that in every row the possiblenum attribute
        is set to [1 to size]
        """
        for row in range(self.size):
            for number in range(self.size):
                if sudoku.editablegrid[row][number].value == 0:
                    sudoku.editablegrid[row][number].possiblenum = list(range(1, sudoku.size + 1))
                else:
                    sudoku.editablegrid[row][number].possiblenum = \
                        [sudoku.editablegrid[row][number].value]
        return sudoku

    def remove_doubles(self, sudoku: Sudoku) -> Sudoku:
        """
        Creates a Sudoko grid where the double values in the possiblenum attribute
        are removed in a single row. So if there is a value 1 in a row,
        every possiblenum attribute is subtracted the possibility of a 1 in that cell.

        Parameters:
        - sudoku: a Sudoku  object
        Returns:
        - sudoku: it changes the Sudoku object that has been inputted
        so that in every row the possiblenum attribute
        is stripped of values that are already in that row
        """
        for row in range(self.size):
            for number in range(1, self.size + 1):
                if number in sudoku.editablegrid[row]:
                    for col in range(sudoku.size):
                        if (number in sudoku.editablegrid[row][col].possiblenum and
                                len(sudoku.editablegrid[row][col].possiblenum) > 1):
                            sudoku.editablegrid[row][col].possiblenum.remove(number)
        return sudoku

    def possibilities(self) -> None:
        """
        Uses almost all previous functions and combines it to get only the possibilities
        that don't conflict with values in every row, column and block.
        So in every cell the row, column and block it is in, is checked whether there
        is a value in one of them that is also in its possiblenum attribute.
        And then that value is removed from their possiblenum so that it has only viable.
        This function creates the foundation that the Hints class is
        based on, because that works with the possible values that can be put in a cell.
        """
        rows_sud = self.remove_doubles(self.all_options(self.sudoku))

        columns_sud = self.row_to_columns(self.remove_doubles(
            self.all_options(self.row_to_columns(self.sudoku))))

        boxes_sud = self.row_to_blocks(self.remove_doubles(
            self.all_options(self.row_to_blocks(self.sudoku))))
        rows = [[y.possiblenum for y in x] for x in rows_sud.editablegrid]
        columns = [[y.possiblenum for y in x] for x in columns_sud.editablegrid]
        boxes = [[y.possiblenum for y in x] for x in boxes_sud.editablegrid]
        new_sudoku = []
        for row in range(self.size):
            new_row = []
            for column in range(self.size):
                if len(rows[row][column]) > 1:
                    if self.variant == 'diagonal' and len(self.get_diagonal(row, column)) > 0:
                        cell = ([value for value in rows[row][column] if
                                 value in columns[row][column] and value in boxes[row][column]])
                        for value in self.get_diagonal(row, column):
                            if value in cell:
                                cell.remove(value.value)
                        new_row.append(cell)

                    elif self.variant == 'chess':
                        cell = ([value for value in rows[row][column] if
                                 value in columns[row][column] and value in boxes[row][column]])
                        for value in self.get_chess(row, column):
                            if value in cell:
                                cell.remove(value.value)
                        new_row.append(cell)

                    else:
                        new_row.append([value for value in rows[row][column] if
                                        value in columns[row][column] and
                                        value in boxes[row][column]])
                else:
                    new_row.append(rows[row][column])
            new_sudoku.append(new_row)
        for x in range(self.sudoku.size):
            for y in range(self.sudoku.size):
                self.sudoku.editablegrid[x][y].possiblenum = new_sudoku[x][y]

    def check_mistake(self) -> bool:
        """
        Checks whether there is a mistake in the sudoku that is provided.
        """
        variants = [self.sudoku, self.row_to_columns(self.sudoku),
                    self.row_to_blocks(self.sudoku)]
        for row in range(self.sudoku.size):
            for column in range(self.sudoku.size):
                if self.variant == 'chess':
                    if self.sudoku.editablegrid[row][column] in self.get_chess(row, column):
                        return False
                elif self.variant == 'diagonal':
                    if (len(self.get_diagonal(row, column)) > 0 and
                            self.get_diagonal(row, column).count(
                                self.sudoku.editablegrid[row][column]) > 1):
                        return False
                for variant in variants:
                    if (variant.editablegrid[row][column] != 0 and
                            variant.editablegrid[row].count(
                                variant.editablegrid[row][column]) != 1):
                        return False
        return True

    def get_sudoku(self) -> Sudoku:
        """
        Makes it easier to print the sudoku, mostly used for testing
        and ease of use when creating Hints class.
        """
        self.possibilities()
        return self.sudoku

    def options(self) -> list[list[list[int]]]:
        """
        Calls possibilities and returns a list that
        contains all possiblenum values in every cell.

        Returns:
        - a list[list[list[int]]]: It contains all possiblenum values in a list
        """
        self.possibilities()
        return [[y.possiblenum for y in x] for x in self.sudoku.editablegrid]

    def values(self) -> list[list[int]]:
        """
        Calls possibilities and returns a list that contains all values in every cell.

        Returns:
        - a list[list[list[int]]]: It contains all values of the sudoku in a list
        """
        self.possibilities()
        return [[y.value for y in x] for x in self.sudoku.editablegrid]
