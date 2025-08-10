import math
import copy
from typing import List, Tuple, Iterator
from project.Hints.basis_matrix import Basis


class Hints:
    """
    A class that can generate different types of hints for a given sudoku.

    Attributes:
    - sudoku (Sudoku object): Creates a Sudoku object with the given Basis object.
    - values (list[list[int]]): It contains all values of the sudoku in a list.
    - posnum (list[list[list[int]]]): It contains all possiblenum values in a list.
    - size (int): The size of the Sudoku grid (default is 9).
    - numbers (list[int]): A list with number from 1 to size of sudoku to
                describe all possible values
    """
    def __init__(self, sudoku: Basis) -> None:
        """
        Initializes a Hints object.

        Parameters:
        - sudoku: Initial Basis configuration
                (a Sudoku object with updated possiblenum values).
        """
        self.sudoku = sudoku
        self.values = sudoku.values()
        self.posnum = sudoku.options()
        self.size = self.sudoku.size
        self.numbers = list(range(1, self.size + 1))

    @staticmethod
    def row_to_columns(sudoku: list[list[list[int]]]) -> list[list[list[int]]]:
        """
        Creates a list where the possible values of 1 column are put in a single list,
        so it transforms the rows into columns.

        Parameters:
        - sudoku: a list of a list that contains every value or every possible value
        Returns:
        - a new list that has the sudoku columns for rows in comparison to the input sudoku
        """
        return [[row[value] for row in sudoku] for value in range(len(sudoku))]

    @staticmethod
    def row_to_blocks(sudoku: list[list[list[int]]]) -> list[list[list[int]]]:
        """
        Creates a list where the possible values of 1 block are put in a single list,
        so it transforms the rows into blocks.

        Parameters:
        - sudoku: a list of a list that contains every value or every possible value
        Returns:
        - a new list that has the sudoku blocks for rows in comparison to the input sudoku
        """
        size = len(sudoku)
        block_size = int(math.sqrt(size))

        blocks = []
        for x in range(0, size, block_size):
            for y in range(0, size, block_size):
                block = [sudoku[row][y: y + block_size] for row in range(x, x + block_size)]
                blocks.append(block)

        new_sudoku = [[cell for sublist in block for cell in sublist] for block in blocks]
        return new_sudoku

    @staticmethod
    def row_to_columns_val(sudoku: list[list[int]]) -> list[list[int]]:
        """
        Creates a list where the values of 1 column are put in a single list,
        so it transforms the rows into columns.

        Parameters:
        - sudoku: a list of a list that contains every value or every possible value
        Returns:
        - a new list that has the sudoku columns for rows in comparison to the input sudoku
        """
        return [[row[value] for row in sudoku] for value in range(len(sudoku))]

    @staticmethod
    def row_to_blocks_val(sudoku: list[list[int]]) -> list[list[int]]:
        """
        Creates a list where the values of 1 block are put in a single list, so it transforms
        the rows into blocks.

        Parameters:
        - sudoku: a list of a list that contains every value or every possible value
        Returns:
        - a new list that has the sudoku blocks for rows in comparison to the input sudoku
        """
        size = len(sudoku)
        block_size = int(math.sqrt(size))

        blocks = []
        for x in range(0, size, block_size):
            for y in range(0, size, block_size):
                block = [sudoku[row][y: y + block_size] for row in range(x, x + block_size)]
                blocks.append(block)

        new_sudoku = [[cell for sublist in block for cell in sublist] for block in blocks]
        return new_sudoku

    @staticmethod
    def combined(sudoku: list[list[list[int]]]) -> List[List[int]]:
        """
        Creates a list where all the possible values of a row are put in a single list,
        so it transforms the inner lists into 1 list.
        This helps the counting of certain values in upcoming hints.

        Parameters:
        - sudoku: a list of a list that contains every possible value
        Returns:
        - a new list that has all possible values of a row in together in a single list
        """
        return [[item for values in row for item in values] for row in sudoku]

    def conv_index_to_coord(self, index: int, form: str) -> list[list[int]]:
        """
        Converts a block, row or column to coordinates in the original sudoku.

        Parameters:
        - index: an integer that is the index of row, column or block
        - form: a string containing whether it is a row, column or block

        Returns:
        - list[list[int]]: the coordinates in a list
        """
        if form == 'block':
            boxes = self.row_to_blocks(self.posnum)
            for position in boxes[index]:
                if isinstance(position, list):
                    position.append(-1)
        elif form == 'row':
            rows = self.posnum
            for position in rows[index]:
                position.append(-1)
        elif form == 'column':
            columns = self.row_to_columns(self.posnum)
            for position in columns[index]:
                if isinstance(position, list):
                    position.append(-1)
        coord = [[y, x] for x in range(len(self.posnum))
                 for y in range(len(self.posnum)) if -1 in self.posnum[y][x]]
        for coordinate in coord:
            self.posnum[coordinate[0]][coordinate[1]].remove(-1)
        return coord

    def conv_coord_to_block(self, coordinates: list[int]) -> int:
        """
        Converts coordinates of a sudoku into the index block.
        So coordinates [2, 2] are in block 0.

        Parameters:
        - coordinates: a list containing the row and column coordinates

        Returns:
        - int: the index of the block
        """
        all_coordinates = [self.conv_index_to_coord(i, 'block') for i in range(self.sudoku.size)]
        for index, coordinate in enumerate(all_coordinates):
            if coordinates in coordinate:
                return index
        return 0

    def hidden_singles(self) -> Iterator[Tuple[str, int, list[list[int]]]]:
        """
        Detects the hidden singles according to sudoku wiki from a sudoku in this class.

        Returns:
        - an iterator of a tuple with 3 items: the type, value, coordinates
        - type: whether it is a row, column or block that has generated the hidden single
        - value: the value that is the single, the value that only has
        1 possible place in this row, column or block
        - coordinates: a list of coordinates that need to be marked in the UI,
        first row then column
        """
        rows = self.posnum
        rows_orig = self.values

        boxes = self.row_to_blocks(self.posnum)
        boxes_orig = self.row_to_blocks_val(self.values)

        columns = self.row_to_columns(self.posnum)
        columns_orig = self.row_to_columns_val(self.values)

        for i in range(len(boxes)):
            counted = [self.combined(boxes)[i].count(number) for number in self.numbers]
            counted_orig = [boxes_orig[i].count(number) for number in self.numbers]
            for value, counted_number in enumerate(counted):
                if (counted_number == 1) and (counted_orig[value] == 0):
                    yield 'block', value + 1, self.conv_index_to_coord(i, 'block')

        for i in range(len(rows)):
            counted = [self.combined(rows)[i].count(number) for number in self.numbers]
            counted_orig = [rows_orig[i].count(number) for number in self.numbers]
            for value, counted_number in enumerate(counted):
                if (counted_number == 1) and (counted_orig[value] == 0):
                    yield 'row', value + 1, self.conv_index_to_coord(i, 'row')

        for i in range(len(columns)):
            counted = [self.combined(columns)[i].count(number) for number in self.numbers]
            counted_orig = [columns_orig[i].count(number) for number in self.numbers]
            for value, counted_number in enumerate(counted):
                if (counted_number == 1) and (counted_orig[value] == 0):
                    yield 'row', value + 1, self.conv_index_to_coord(i, 'column')

    def conjugatepairs(self) -> Iterator[tuple[str, tuple[str, int],
                                         list[tuple[list[int], list[int]]]]]:
        """
        Detects the naked doubles, triples and quadruples according to
        sudoku wiki from a sudoku in this class.

        Returns:
        - an iterator of a tuple with 3 items: the type, value, coordinates
        - type: whether it is a row, column or block that has generated the pair
        - kind: wheter it is a double, triple or quad
        - tuples containing the coordinates and notes: the coordinates of
        the cell and the notes that need to be inputted
        """
        sort_list = ['row', 'column', 'block']
        all_options = [self.posnum, self.row_to_columns(self.posnum),
                       self.row_to_blocks(self.posnum)]

        pair_list = [('double', 0), ('triple', 1), ('quad', 2)]
        for sort_typecount, sort_type in enumerate(all_options):
            for i, structure in enumerate(sort_type):
                marked = []
                current = structure
                for pair_type in range(2, 5, 1):
                    for x, row in enumerate(current):
                        tempmarked = []
                        counter = 0
                        if len(row) == pair_type and x not in marked:
                            for y, col in enumerate(current):
                                amount_same_num = len(set(row) & set(col))
                                if (pair_type >= len(col) == amount_same_num >= 2 and
                                        y not in marked):
                                    counter += 1
                                    tempmarked.append(y)
                        if counter == pair_type:
                            marked += tempmarked
                            coord = self.conv_index_to_coord(i, sort_list[sort_typecount])
                            if sort_list[sort_typecount] == 'block':
                                coord = sorted(self.conv_index_to_coord(
                                    i, sort_list[sort_typecount]), key=lambda z: (z[0], z[1]))
                            coordlist = [coord[p] for p in range(len(coord)) if p in marked]
                            poslist = [current[p] for p in range(len(coord)) if p in marked]
                            yield (sort_list[sort_typecount], pair_list[pair_type-2],
                                   list(zip(coordlist, poslist)))

    def sort_conjpairs(self) -> Iterator[tuple[str, tuple[str, int],
                                         list[tuple[list[int], list[int]]]]]:
        """
        Gets all the naked / conjugate pairs and sorts them by pair type so
        first doubles, then triples, then quads.

        Returns:
        - an iterator of a tuple with 3 items: the type, value, coordinates
        - type: whether it is a row, column or block that has generated the pair
        - kind: wheter it is a double, triple or quad
        - tuples containing the coordinates and notes: the coordinates of
        the cell and the notes that need to be inputted
        """
        list_conj = list(self.conjugatepairs())
        sortedbypair_type = sorted(list_conj, key=lambda x: x[1][1])
        for i in sortedbypair_type:
            yield i

    def hidden_pairs(self) -> Iterator[List[List[int]]]:
        """
        Detects the hidden pairs, triples and quadruples according to
        sudoku wiki from a sudoku in this class.

        Returns:
        - an iterator of 2 or 3 lists inside a list depending on if it is a pair or a triple:
        Each innerlist consists of a few values, the first two are the coordinates in the sudoku,
        first the row and then the column.
        The next values are the nodes that are true to those coordinates.
        """
        variants = [self.row_to_blocks(self.posnum), self.row_to_columns(self.posnum), self.posnum]
        variants_names = ['block', 'column', 'row']
        output = []
        for form, structure in enumerate(variants):
            for i in range(len(structure)):
                counted = [self.combined(structure)[i].count(number) for
                           number in self.numbers]
                if counted.count(2) >= 2:
                    pair = [value + 1 for value in range(len(counted)) if counted[value] == 2]
                else:
                    pair = [value + 1 for value in range(len(counted)) if 1 < counted[value] < 5
                            and (counted.count(2) + counted.count(3) + counted.count(4)) >= 2]

                all_coord = sorted(self.conv_index_to_coord(i, variants_names[form]),
                                   key=lambda z: (z[0], z[1]))
                cells = [(cell, all_coord[i]) for i, cell in enumerate(structure[i])
                         for number in pair if number in cell]

                coordinates = [cell[1] for cell in cells]
                posnums = [cell[0] for cell in cells]
                posnums_corr = []
                mult_coord = []

                for x, coordinate in enumerate(coordinates):
                    if (not coordinates.count(coordinate) < 2 and
                            coordinate not in mult_coord):
                        mult_coord.append(coordinate)
                        posnums_corr.append(posnums[x])

                combined_posnums = [item for values in posnums_corr for item in values]
                pair_corr = []
                new_posnums = copy.deepcopy(posnums_corr)
                for value in pair:
                    if combined_posnums.count(value) == counted[value - 1]:
                        pair_corr.append(value)
                    else:
                        for note in new_posnums:
                            if value in note:
                                note.remove(value)

                if 1 < len(pair_corr) < 5 and len(pair_corr) == len(mult_coord):
                    for value in self.numbers:
                        for index, posnum in enumerate(new_posnums):
                            if value in posnum and value not in pair_corr:
                                posnum.remove(value)
                    new_pair = [mult_coord[index] + new_posnums[index] for
                                index in range(len(pair_corr))]
                    output.append(new_pair)

        correct_output = []
        for outcome in output:
            if outcome not in correct_output:
                correct_output.append(outcome)
        for new_hint in correct_output:
            yield new_hint

    def pointing_pairs(self) -> Iterator[Tuple[List[int], int, str]]:
        """
        Detects pointing pairs and triples according to sudoku wiki from a sudoku in this class.

        Returns:
        - an iterator of a tuple of 3 items: coordinates, the value and the sort of pair
        - coordinates: a list with row and column coordinates of the cell that needs to be adjusted
        - the value: the value that needs to be removed from the notes in the regarding cell
        - sort of pair: whether it is a pointing pair in column or row direction
        """
        variants = {'block': self.row_to_blocks(self.posnum),
                    'column': self.row_to_columns(self.posnum), 'row': self.posnum}
        for i in range(len(variants['block'])):
            counted = [self.combined(variants['block'])[i].count(number)
                       for number in self.numbers]

            all_coordinates = sorted(self.conv_index_to_coord(i, 'block'),
                                     key=lambda z: (z[0], z[1]))
            for number in range(1, len(counted) + 1):
                if counted[number - 1] == 2 or counted[number - 1] == 3:
                    indices = []
                    for index in range(len(variants['block'][i])):
                        if number in variants['block'][i][index]:
                            indices.append(all_coordinates[index])

                    check_row = [index[0] for index in indices]
                    if len(set(check_row)) == 1:
                        for row in check_row:
                            if check_row.count(row) > 1:
                                coord_row = self.conv_index_to_coord(row, 'row')
                                for y in range(len(variants['row'])):
                                    if (number in variants['row'][row][y] and
                                            coord_row[y] not in indices):
                                        yield coord_row[y], number, 'row'
                            break

                    check_col = [index[1] for index in indices]
                    if len(set(check_col)) == 1:
                        for col in check_col:
                            if check_col.count(col) > 1:
                                coord_col = self.conv_index_to_coord(col, 'column')
                                for y in range(len(variants['column'])):
                                    if (number in variants['column'][col][y] and
                                            coord_col[y] not in indices):
                                        yield coord_col[y], number, 'column'
                            break

    def box_line_reduction(self) -> Iterator[Tuple[List[int], int, str]]:
        """
        Detects box line reduction values according to sudoku wiki from a sudoku in this class.

        Returns:
        - an iterator of a tuple of 3 items: coordinates, the value and the sort of pair
        - coordinates: a list with row and column coordinates of the cell that needs to be adjusted
        - the value: the value that needs to be removed from the notes in the regarding cell
        - sort of pair: whether it is a box line reduction via column or row direction
        """
        variants = {'block': self.row_to_blocks(self.posnum),
                    'column': self.row_to_columns(self.posnum), 'row': self.posnum}
        types = ['row', 'column']

        for form in types:
            for i in range(len(variants[form])):
                counted = [self.combined(variants[form])[i].count(number) for
                           number in self.numbers]
                all_coordinates = self.conv_index_to_coord(i, form)
                for number in range(1, len(counted) + 1):
                    if counted[number - 1] == 2 or counted[number - 1] == 3:
                        indices = []
                        for index in range(len(variants[form][i])):
                            if number in variants[form][i][index]:
                                indices.append(all_coordinates[index])
                        coord_index = self.conv_coord_to_block(indices[0])

                        coord_block = sorted(self.conv_index_to_coord(coord_index, 'block'),
                                             key=lambda z: (z[0], z[1]))
                        if all(coord in coord_block for coord in indices):
                            for y in range(len(variants['block'])):
                                if (number in variants['block'][coord_index][y] and
                                        coord_block[y] not in indices):
                                    yield coord_block[y], number, f'block via {form}'
