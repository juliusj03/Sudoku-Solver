import copy
import pytest
from project.Sudoku.Sudoku import Sudoku, Cell
from project.solver.solver import Solver

# Test data
sample_sudoku_data = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

@pytest.fixture
def sample_sudoku():
    return Sudoku(copy.deepcopy(sample_sudoku_data))

@pytest.fixture
def sample_sudokunone():
    return Sudoku()

def test_Solver_init(sample_sudoku, sample_sudokunone):
    """Test the fillcoor method.

    Parameters:
    - sample_sudoku (Sudoku): An initialized Sudoku instance for testing.
    - sample_sudokunone (Sudoku): An initialized Sudoku instance for testing with no parameters.
    """
    assert sample_sudoku.editablegrid != sample_sudoku.emptygrid, 'Incorrect comparison, expected True'
    assert sample_sudokunone.editablegrid == sample_sudokunone.emptygrid, 'Incorrect comparison, expected True'

def test_fillcoor(sample_sudoku):
    """Test the fillcoor method.

    Parameters:
    - sample_sudoku (Sudoku): An initialized Sudoku instance for testing.
    """
    sample_sudoku.fillcoor(4, 0, 2)
    assert sample_sudoku.originalgrid[0][2] == 4, 'Incorrect value for row, col (0, 2), expected 4'
    assert sample_sudoku.solutiongrid[0][2] == 4, 'Incorrect value for row, col (0, 2), expected 4'


def test_fillcooruser(sample_sudoku):
    """Test the fillcooruser method.

    Parameters:
    - sample_sudoku (Sudoku): An initialized Sudoku instance for testing.
    """
    sample_sudoku.fillcooruser(6, 1, 1)
    assert sample_sudoku.editablegrid[1][1] == 6, 'Incorrect value for row, col (1, 1), expected 6'
    sample_sudoku.fillcooruser(Cell(6), 1, 1)
    assert sample_sudoku.editablegrid[1][1] == 6, 'Incorrect value for row, col (1, 1), expected 6'


def test_repr(sample_sudoku):

    assert (repr(sample_sudoku) == """---------------------------
 5 3 0 | 0 7 0 | 0 0 0
 6 0 0 | 1 9 5 | 0 0 0
 0 9 8 | 0 0 0 | 0 6 0
---------------------------
 8 0 0 | 0 6 0 | 0 0 3
 4 0 0 | 8 0 3 | 0 0 1
 7 0 0 | 0 2 0 | 0 0 6
---------------------------
 0 6 0 | 0 0 0 | 2 8 0
 0 0 0 | 4 1 9 | 0 0 5
 0 0 0 | 0 8 0 | 0 7 9
---------------------------
""")


def test_comparetoanswer(sample_sudoku):
    """Test the comparetoanswer method.

    Parameters:
    - sample_sudoku (Sudoku): An initialized Sudoku instance for testing.
    """
    solved = Solver(sample_sudoku)
    solved.solvebrute()
    result, row, col = sample_sudoku.comparetoanswer()
    assert result, 'Incorrect value for result, expected True'
    assert row == 0, 'Incorrect value for result, expected 0'
    assert col == 0, 'Incorrect value for result, expected 0'


def test_printsolution(sample_sudoku, capsys):
    solved = Solver(sample_sudoku)
    solved.solvebrute()
    printed_solution = sample_sudoku.printsolution()
    assert ("""---------------------------
 5 3 4 | 6 7 8 | 9 1 2
 6 7 2 | 1 9 5 | 3 4 8
 1 9 8 | 3 4 2 | 5 6 7
---------------------------
 8 5 9 | 7 6 1 | 4 2 3
 4 2 6 | 8 5 3 | 7 9 1
 7 1 3 | 9 2 4 | 8 5 6
---------------------------
 9 6 1 | 5 3 7 | 2 8 4
 2 8 7 | 4 1 9 | 6 3 5
 3 4 5 | 2 8 6 | 1 7 9
---------------------------
"""==printed_solution)


def test_sudoku_eq(sample_sudoku):
    # Test the __eq__ method
    sudoku_copy = Sudoku(copy.deepcopy(sample_sudoku_data))
    assert sample_sudoku == sudoku_copy, 'Incorrect comparison, expected True'


def test_cell_init():
    # Test initialization of Cell instance
    sample_cell = Cell(3)
    assert sample_cell.value == 3,'Incorrect value for self.value, expected 3'


def test_cell_value_setter():
    # Test the value setter in Cell
    sample_cell = Cell(3)
    sample_cell.value = 5
    assert sample_cell.value == 5,'Incorrect value for self.value, expected 5'

def test_cell_remove():
    # Test the remove method in Cell
    sample_cell = Cell(3)
    sample_cell.possiblenum = [3,2]
    sample_cell.remove(3)
    assert 3 not in sample_cell.possiblenum,'Incorrect value for self.value, expected [2]'


def test_cell_eq():
    # Test the __eq__ method in Cell
    sample_cell = Cell(3)
    assert sample_cell == 3,'Incorrect value for self.value, expected 3'
    other_cell = Cell(3)
    assert sample_cell == other_cell, 'Incorrect value for self.value, expected 3'
    with pytest.raises(ValueError):
        sample_cell == 'iets'