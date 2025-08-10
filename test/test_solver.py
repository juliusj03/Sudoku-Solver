from unittest.mock import patch
import pytest
from project.Sudoku.Sudoku import Sudoku, Cell
from project.solver.solver import Solver

PATH = "project.solver.solver."


@pytest.fixture
def Solver_inst_param(request):
    """Creates an initialized Solver class with specified parameters"""
    sudoku_data = request.param
    mode = 0
    sud = Sudoku(sudoku_data)
    return Solver(sud, mode)


@pytest.fixture
def Solver_inst():
    """Creates an initialized Solver class with specified parameters"""
    sudoku = [
        [6, 0, 0, 0, 0, 0, 0, 1, 0],
        [8, 0, 0, 0, 0, 4, 0, 0, 0],
        [0, 4, 0, 0, 6, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 8, 0, 0, 7],
        [0, 3, 0, 0, 0, 0, 2, 8, 4],
        [1, 0, 2, 0, 0, 0, 3, 0, 0],
        [4, 0, 6, 7, 5, 0, 0, 0, 0],
        [0, 1, 5, 0, 8, 0, 6, 0, 0],
        [0, 0, 8, 3, 1, 0, 5, 0, 0],
    ]
    mode = 0
    return Solver(Sudoku(sudoku), mode)

@pytest.fixture
def Solver_instmode1():
    """Creates an initialized Solver class with specified parameters"""
    sudoku = [
        [6, 0, 0, 0, 0, 0, 0, 1, 0],
        [8, 0, 0, 0, 0, 4, 0, 0, 0],
        [0, 4, 0, 0, 6, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 8, 0, 0, 7],
        [0, 3, 0, 0, 0, 0, 2, 8, 4],
        [1, 0, 2, 0, 0, 0, 3, 0, 0],
        [4, 0, 6, 7, 5, 0, 0, 0, 0],
        [0, 1, 5, 0, 8, 0, 6, 0, 0],
        [0, 0, 8, 3, 1, 0, 5, 0, 0],
    ]
    mode = 1
    return Solver(Sudoku(sudoku), mode)

@pytest.fixture
def Solver_instmode2():
    """Creates an initialized Solver class with specified parameters"""
    sudoku = [
        [6, 0, 0, 0, 0, 0, 0, 1, 0],
        [8, 0, 0, 0, 0, 4, 0, 0, 0],
        [0, 4, 0, 0, 6, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 8, 0, 0, 7],
        [0, 3, 0, 0, 0, 0, 2, 8, 4],
        [1, 0, 2, 0, 0, 0, 3, 0, 0],
        [4, 0, 6, 7, 5, 0, 0, 0, 0],
        [0, 1, 5, 0, 8, 0, 6, 0, 0],
        [0, 0, 8, 3, 1, 0, 5, 0, 0],
    ]
    mode = 2
    return Solver(Sudoku(sudoku), mode)


def test_Solver_init(Solver_inst, Solver_instmode1, Solver_instmode2):
    """Test for the initialization of the Solver Class"""
    solverinst = Solver_inst
    solverinst1 = Solver_instmode1
    solverinst2 = Solver_instmode2
    assert solverinst.mode == 0, "Incorrect value for self.mode, expected 0"
    assert solverinst1.mode == 1, "Incorrect value for self.mode, expected 1"
    assert solverinst2.mode == 2, "Incorrect value for self.mode, expected 2"
    assert solverinst.basismode == 'standard', "Incorrect value for self.mode, expected standard"
    assert solverinst1.basismode == 'diagonal', "Incorrect value for self.mode, expected diagonal"
    assert solverinst2.basismode == 'chess', "Incorrect value for self.mode, expected chess"
    assert solverinst.iteration == 0, "Incorrect value for self.iteration, expected 0"
    assert (
        solverinst.solutionbool is False
    ), "Incorrect value for self.solutionbool, expected False"


@pytest.mark.parametrize(
    "Solver_inst_param",
    [
        [
            [6, 0, 0, 0, 0, 0, 0, 1, 0],
            [8, 0, 0, 0, 0, 4, 0, 0, 0],
            [0, 4, 0, 0, 6, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 8, 0, 0, 7],
            [0, 3, 0, 0, 0, 0, 2, 8, 4],
            [1, 0, 2, 0, 0, 0, 3, 0, 0],
            [4, 0, 6, 7, 5, 0, 0, 0, 0],
            [0, 1, 5, 0, 8, 0, 6, 0, 0],
            [0, 0, 8, 3, 1, 0, 5, 0, 0],
        ],
        [
            [6, 6, 6, 0, 0, 0, 0, 1, 0],
            [8, 0, 0, 0, 0, 4, 0, 0, 0],
            [0, 4, 0, 0, 6, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 8, 0, 0, 7],
            [0, 3, 0, 0, 0, 0, 2, 8, 4],
            [1, 0, 2, 0, 0, 0, 3, 0, 0],
            [4, 0, 6, 7, 5, 0, 0, 0, 0],
            [0, 1, 5, 0, 8, 0, 6, 0, 0],
            [0, 0, 8, 3, 1, 0, 5, 0, 0],
        ],
    ],
    indirect=True,
)
def test_solvebrute(Solver_inst_param):
    """Checks if the solvebrute function works accordingly and solves the sudoku"""
    Solverinst = Solver_inst_param
    Solved = Solverinst.solvebrute()
    if Solverinst.sudoku.originalgrid[0][1] == 6:
        assert (
            Solverinst.solutionbool is False
        ), "Incorrect value for self.solutionbool, expected False"
        assert Solved is False, "Incorrect value for self.solutionbool, expected False"
    else:
        assert (
            Solverinst.solutionbool is True
        ), "Incorrect value for self.solutionbool, expected True"
        assert Solved is True, "Incorrect value for self.solutionbool, expected True"


@pytest.mark.parametrize(
    "Solver_inst_param",
    [
        [
            [6, 0, 0, 0, 0, 0, 0, 1, 0],
            [8, 0, 0, 0, 0, 4, 0, 0, 0],
            [0, 4, 0, 0, 6, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 8, 0, 0, 7],
            [0, 3, 0, 0, 0, 0, 2, 8, 4],
            [1, 0, 2, 0, 0, 0, 3, 0, 0],
            [4, 0, 6, 7, 5, 0, 0, 0, 0],
            [0, 1, 5, 0, 8, 0, 6, 0, 0],
            [0, 0, 8, 3, 1, 0, 5, 0, 0],
        ],
        [
            [6, 2, 3, 9, 7, 5, 4, 1, 8],
            [8, 5, 9, 1, 2, 4, 7, 6, 3],
            [7, 4, 1, 8, 6, 3, 9, 2, 5],
            [9, 6, 4, 2, 3, 8, 1, 5, 7],
            [5, 3, 7, 6, 9, 1, 2, 8, 4],
            [1, 8, 2, 5, 4, 7, 3, 9, 6],
            [4, 9, 6, 7, 5, 2, 8, 3, 1],
            [3, 1, 5, 4, 8, 9, 6, 7, 2],
            [2, 7, 8, 3, 1, 6, 5, 4, 9],
        ],
    ],
    indirect=True,
)
def test_getcellpos(Solver_inst_param):
    """Checks getcellpos returns the next 0 in the sudoku

    Parameters
    ----------
    Solver_inst_param: Solver
        Creates an initiliazed Solver class wit specified parameters
    sudoku: Sudoku
        used to check multiple sudokus for different tests and outcomes
    """
    Solverinst = Solver_inst_param
    position = Solverinst.getcellpos()
    if Solverinst.sudoku.originalgrid[0][1] == 2:
        assert position is None, "Incorrect value for (row, col), expected None"
    else:
        assert position == (0, 1), "Incorrect value for (row, col), expected (0,1)"


def test_ruleset(Solver_inst, Solver_instmode1, Solver_instmode2):
    """Checks if the inserted number is possible in for the specified ruleset

    Parameters
    ----------
    Solver_inst: Solver
        Creates an initiliazed Solver class wit specified parameters
    Solver_instmode1: Solver
        Creates an initiliazed Solver class wit specified parameters using mode 1
    Solver_instmode1: Solver
        Creates an initiliazed Solver class wit specified parameters using mode 2
    """
    Solverinst = Solver_inst
    Solverinstmode1 = Solver_instmode1
    Solverinstmode2 = Solver_instmode2
    notpossible = Solverinst.ruleset((0, 1), 6)
    possible = Solverinst.ruleset((0, 1), 2)
    notpossible1 = Solverinstmode1.diagonalcheck(1, 1, 6)
    possible1 = Solverinstmode1.diagonalcheck(1, 1, 2)
    notpossible2 = Solverinstmode2.chesscheck(1, 2, 6)
    possible2 = Solverinstmode2.chesscheck(1, 2, 2)
    assert possible is True, "Incorrect value for self.solutionbool, expected True"
    assert notpossible is False, "Incorrect value for self.solutionbool, expected False"
    assert possible1 is True, "Incorrect value for self.solutionbool, expected True"
    assert notpossible1 is False, "Incorrect value for self.solutionbool, expected False"
    assert possible2 is True, "Incorrect value for self.solutionbool, expected True"
    assert notpossible2 is False, "Incorrect value for self.solutionbool, expected False"


def test_colcheck(Solver_inst):
    """Checks if the inserted number is possible in the column

    Parameters
    ----------
    Solver_inst: Solver
        Creates an initiliazed Solver class wit specified parameters
    """
    Solverinst = Solver_inst
    notpossible = Solverinst.colcheck(0, 1, 4)
    possible = Solverinst.colcheck(0, 1, 2)
    assert possible is True, "Incorrect value for self.solutionbool, expected True"
    assert notpossible is False, "Incorrect value for self.solutionbool, expected False"


def test_rowcheck(Solver_inst):
    """Checks if the inserted number is possible in the row

    Parameters
    ----------
    Solver_inst: Solver
        Creates an initiliazed Solver class wit specified parameters
    """
    Solverinst = Solver_inst
    notpossible = Solverinst.rowcheck(0, 1, 6)
    possible = Solverinst.rowcheck(0, 1, 2)
    assert possible is True, "Incorrect value for self.solutionbool, expected True"
    assert notpossible is False, "Incorrect value for self.solutionbool, expected False"


def test_blockcheck(Solver_inst):
    """Checks if the inserted number is possible in the block

    Parameters
    ----------
    Solver_inst: Solver
        Creates an initiliazed Solver class wit specified parameters
    """
    Solverinst = Solver_inst
    notpossible = Solverinst.blockcheck(0,1, 6)
    possible = Solverinst.blockcheck(0,1, 2)
    assert possible is True, 'Incorrect value for self.solutionbool, expected True'
    assert notpossible is False, 'Incorrect value for self.solutionbool, expected False'

def test_diagonalcheck(Solver_inst):
    """Checks if the inserted number is possible in the diagonal

    Parameters
    ----------
    Solver_inst: Solver
        Creates an initiliazed Solver class wit specified parameters
    """
    Solverinst = Solver_inst
    notpossible = Solverinst.diagonalcheck(1, 1, 6)
    notpossible2 = Solverinst.diagonalcheck(0, 8, 8)
    possible = Solverinst.diagonalcheck(1, 1, 2)
    possible2 = Solverinst.diagonalcheck(0, 8, 2)
    assert possible is True, 'Incorrect value for self.solutionbool, expected True'
    assert notpossible is False, 'Incorrect value for self.solutionbool, expected False'
    assert possible2 is True, 'Incorrect value for self.solutionbool, expected True'
    assert notpossible2 is False, 'Incorrect value for self.solutionbool, expected False'

def test_chesscheck(Solver_inst):
    """Checks if the inserted number is possible within chess knight moves

    Parameters
    ----------
    Solver_inst: Solver
        Creates an initiliazed Solver class wit specified parameters
    """
    Solverinst = Solver_inst
    notpossible = Solverinst.chesscheck(1, 2, 6)
    possible = Solverinst.chesscheck(1, 2, 2)
    assert possible is True, 'Incorrect value for self.solutionbool, expected True'
    assert notpossible is False, 'Incorrect value for self.solutionbool, expected False'