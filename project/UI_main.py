'''This file contains all code used to launch the UI'''
import sys
import time
import os
from PySide6 import QtWidgets as qtw
from PySide6.QtCore import QObject, QEvent, Qt, QTimer
from PySide6.QtGui import QValidator, QPixmap

# Imports related to the ui
from project.UI_sudoku.ui_main_window import Ui_Mainwindow
from project.UI_sudoku.ui_sudoku_upload_grid import Ui_UploadWindow
from project.UI_sudoku.ui_sudoku_playing_grid import Ui_PlayingWindow
from project.UI_sudoku.ui_confirm_return_to_main import Ui_ConfirmToMain
from project.UI_sudoku.ui_sudoku_winner import Ui_WinnerWindow
from project.UI_sudoku.ui_size_selection_screen import Ui_SelectionScreen
from project.UI_sudoku.ui_sudoku_upload_grid_16x16 import Ui_UploadWindow16x16
from project.UI_sudoku.ui_sudoku_upload_grid_4x4 import Ui_UploadWindow4x4
from project.UI_sudoku.ui_not_solvable import Ui_IncorrectSolution
from project.UI_sudoku.ui_sudoku_playing_grid_4x4 import Ui_PlayingWindow4x4
from project.UI_sudoku.ui_sudoku_playing_grid_16x16 import Ui_PlayingWindow16x16
from project.UI_sudoku.ui_information_screen import Ui_Information
from project.UI_sudoku.ui_no_hint_available import Ui_no_hint_available
from project.UI_sudoku.ui_no_hint_mistake import Ui_no_hint_mistake
from project.UI_sudoku.ui_size_selection_screen_generator import Ui_SelectionScreenGenerator
from project.UI_sudoku.ui_not_unique import Ui_SeveralSolution

# Non ui related files
from project.generator.generator import Generator
from project.Sudoku.Sudoku import Sudoku
from project.solver.solver import Solver
from project.Hints.basis_matrix import Basis
from project.Hints.hints import Hints


sys.setrecursionlimit(15000)

def index_to_cell(row, column):
    """turns the coordinates of a cell into the appropriate object name"""
    string = f'le_{str(column).zfill(2)}_{str(row).zfill(2)}'
    return string

def index_to_note(row, column):
    """turns the coordinates of a cell into appropriate notes_label name"""
    string = f'nt_{str(column).zfill(2)}_{str(row).zfill(2)}'
    return string

def create_all_cells(size: int) -> list[str]:
    """creates a list of all the cells that are present in the sudoku grid"""
    result = []
    for i in range(size):
        for x in range(size):
            string = f'le_{str(i).zfill(2)}_{str(x).zfill(2)}'
            result.append(string)

    return result

def create_all_notes(size: int, obj: object) -> list[str]:
    """creates a  list of all the note_labels that are present in the
        sudoku grid, and sets their contents blank"""
    result = []
    for row in range(size):
        for column in range(size):
            string = index_to_note(row, column)
            result.append(string)

    for note in result:
        getattr(obj, note).setText('')

    return result

def set_up_sudoku_grid(object, size):
    ''''Includes all code associated with configuring a sudoku grid'''
    def set_cell(le_x, size):
        '''''restricts the input of a cell'''
        class CustomValidator(QValidator):
            ''''validates whether the input is within bounds'''
            def validate(self, input_str, pos):

                if not input_str:
                    return QValidator.Intermediate, input_str, pos

                try:
                    value = int(input_str)
                    if 1 <= value <= size:
                        return QValidator.Acceptable, input_str, pos
                    return QValidator.Invalid, input_str, pos
                except ValueError:
                    return QValidator.Invalid, input_str, pos

        numeric_validator = CustomValidator()
        if size < 10:
            le_x.setMaxLength(1)
        else:
            le_x.setMaxLength(2)
        le_x.setValidator(numeric_validator)

    class MyEventFilter(QObject):
        ''''Involved with determining which cell is being altered on the sudoku grid'''

        def eventFilter(self, obj, event):
            if event.type() == QEvent.FocusIn:
                object.cell_in_focus = (int(obj.objectName()[3:5]), int(obj.objectName()[6:]))
            return super().eventFilter(obj, event)

    event_filter = MyEventFilter(object)

    # line of code to ensure that all cells in the grid record their position and user input.
    # this loop can also be used to affect the aesthetics of all cells at once.
    for cell in object.all_cells:
        # cell functionality
        set_cell(getattr(object, cell), size)
        getattr(object, cell).installEventFilter(event_filter)
        getattr(object, cell).textEdited[str].connect(lambda text: object.cell_into_grid(text))

        # cell aesthetics
        if (object.mode == 'diagonal' and
        (cell[3:5] == cell[6:] or (int(cell[3:5]) + int(cell[6:]) == size - 1))):
            getattr(object, cell).setStyleSheet("QLineEdit{\n"
                                                "background-color: rgba(203, 203, 203, 99);\n"
                                                "}\n"
                                                "QLineEdit:focus {\n"
                                                "	background-color: rgba(163, 223, 249, 99);\n"
                                                "}")
        else:
            getattr(object, cell).setStyleSheet("QLineEdit{\n"
                                                "background-color: rgba(255, 255, 255, 0);\n"
                                                "}\n"
                                                "QLineEdit:focus {\n"
                                                "	background-color: rgba(163, 223, 249, 99);\n"
                                                "}")

class MainWindow(qtw.QWidget, Ui_Mainwindow):
    """The initial window when you run the program"""
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.button1.clicked.connect(self.open_selection_window)
        self.button2.clicked.connect(self.open_selection_window_generator)
        self.show()


    def open_selection_window(self):
        """takes user to the size selection screen"""
        self.selection_window = SizeSelection()
        self.selection_window.setAttribute(Qt.WA_DeleteOnClose)
        self.selection_window.show()
        self.close()

    def open_selection_window_generator(self):
        """takes user to the size selection screen for the generator"""
        self.selection_window_gen = SizeSelectionGenerator()
        self.selection_window_gen.setAttribute(Qt.WA_DeleteOnClose)
        self.selection_window_gen.show()
        self.close()

class UploadMaster(qtw.QWidget):
    """Parent class for the upload screens"""

    def notify_uploading(self, mode=0, override=False):
        """An interim function that indicates the user that the program is solving the sudoku.
        The open_playing_window function is opened after a short delay. The delay is necessary
        for the indication to become visible."""
        self.upload_button.setText('Uploading...')
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.setSingleShot(True)
        self.timer.start()
        self.timer.timeout.connect(lambda: self.open_playing_window(mode, override))

    def open_playing_window(self, mode=0, override=False):
        ''''opens up the playing window when button is hit. Calls upon the Solver to find the
            solution for the uploaded sudoku. Override is set to true if the user does not
            mind playing a sudoku which is not unique.
        '''
        variants = ['standard', 'diagonal', 'chess']
        self.sudoku_game = Sudoku(self.sudoku_game.originalgrid, self.sudoku_game.size)
        mistake_check = Basis(self.sudoku_game, variant=variants[mode])
        if not mistake_check.check_mistake():
            solvable = False
        else:
            solver = Solver(self.sudoku_game, mode)
            solver.solvebrute()
            solvable = solver.solutionbool
        if not solvable:
            self.upload_button.setText('Upload my Sudoku!')
            self.incorrect_window = NotSolvable()
            self.incorrect_window.setAttribute(Qt.WA_DeleteOnClose)
            self.incorrect_window.show()
        else:
            unique = False
            if not override:
                gen = Generator(self.sudoku_game, variant=self.mode)
                unique = gen.solution_is_unique(self.sudoku_game.originalgrid)
            if unique or override:
                if self.sudoku_game.size == 4 and mode == 0:
                    self.playing_window = PlayingWindow4x4(self.sudoku_game)
                elif self.sudoku_game.size == 9 and mode == 0:
                    self.playing_window = PlayingWindow9x9(self.sudoku_game)
                elif self.sudoku_game.size == 16 and mode == 0:
                    self.playing_window = PlayingWindow16x16(self.sudoku_game)
                elif self.sudoku_game.size == 9 and mode == 1:
                    self.playing_window = PlayingWindowDiagonal9x9(self.sudoku_game)
                elif self.sudoku_game.size == 4 and mode == 1:
                    self.playing_window = PlayingWindowDiagonal4x4(self.sudoku_game)
                elif self.sudoku_game.size == 16 and mode == 1:
                    self.playing_window = PlayingWindowDiagonal16x16(self.sudoku_game)
                elif self.sudoku_game.size == 9 and mode == 2:
                    self.playing_window = PlayingWindowChess9x9(self.sudoku_game)
                elif self.sudoku_game.size == 4 and mode == 2:
                    self.playing_window = PlayingWindowChess4x4(self.sudoku_game)
                elif self.sudoku_game.size == 16 and mode == 2:
                    self.playing_window = PlayingWindowChess16x16(self.sudoku_game)
                self.playing_window.setAttribute(Qt.WA_DeleteOnClose)
                self.playing_window.show()
                self.close()
            else:
                self.upload_button.setText('Upload my Sudoku!')
                self.not_unique_window = NotUnique(self, self.sudoku_game, mode)
                self.not_unique_window.setAttribute(Qt.WA_DeleteOnClose)
                self.not_unique_window.show()


    def return_to_main_window(self):
        """Opens up a confirmation window when the user wants to return to the main menu"""
        self.confirm = ConfirmToMain(self)
        self.confirm.setAttribute(Qt.WA_DeleteOnClose)
        self.confirm.show()

    def cell_into_grid(self, number) -> None:
        """Stores the number entered by the user in the corresponding position in the original- and
        editablegrid of the Sudoku class object. We use the attribute of a child class since
        UploadMaster has no init method, so we use ignore[attr-defined] to disable the mypy error.
        """
        pos = self.cell_in_focus                                        # type: ignore[attr-defined]
        if number == '':
            self.sudoku_game.fillcoor(0, pos[1], pos[0])
            self.sudoku_game.fillcooruser(0, pos[1], pos[0])
        else:
            self.sudoku_game.fillcoor(int(number), pos[1], pos[0])
            self.sudoku_game.fillcooruser(int(number), pos[1], pos[0])

    def fill_upload_field(self):
        """turns the numbers entered on the upload screen permanent: so that they can't be changed
            accidentally"""
        for column in range(self.sudoku_game.size):
            for row in range(self.sudoku_game.size):
                number = self.sudoku_game._originalgrid[row][column]
                if number != 0:
                    string = index_to_cell(row, column)
                    #string = f'le_{row}{column}'
                    getattr(self, string).setText(str(number))

class Upload9x9(UploadMaster, Ui_UploadWindow):
    """the window used to upload sudokus"""
    def __init__(self, sudoku: Sudoku|None = None):
        super().__init__()

        self.setupUi(self)
        if sudoku is None:
            self.sudoku_game = Sudoku(size = 9)
        else:
            self.sudoku_game = Sudoku(sudoku.originalgrid, sudoku.size)
            self.fill_upload_field()
        self.mode = 'standard'
        self.all_cells = create_all_cells(9)
        self.cell_in_focus = (0, 0)
        set_up_sudoku_grid(self, 9)

        self.return_button.clicked.connect(self.return_to_main_window)
        self.upload_button.clicked.connect(self.notify_uploading)

class Upload4x4(UploadMaster, Ui_UploadWindow4x4):
    """the window used to upload sudokus"""
    def __init__(self, sudoku: Sudoku|None = None):
        super().__init__()
        self.setupUi(self)
        if sudoku is None:
            self.sudoku_game = Sudoku(size = 4)
        else:
            self.sudoku_game = Sudoku(sudoku.originalgrid, sudoku.size)
            self.fill_upload_field()
        self.mode = 'standard'
        self.all_cells = create_all_cells(4)
        self.cell_in_focus = (0, 0)
        self.playing_window = None
        set_up_sudoku_grid(self, 4)

        self.return_button.clicked.connect(self.return_to_main_window)
        self.upload_button.clicked.connect(self.notify_uploading)

class Upload16x16(UploadMaster, Ui_UploadWindow16x16):
    """the window used to upload 16x16 sudokus"""
    def __init__(self, sudoku: Sudoku|None = None):
        super().__init__()
        self.setupUi(self)
        if sudoku is None:
            self.sudoku_game = Sudoku(size=16)
        else:
            self.sudoku_game = Sudoku(sudoku.originalgrid, sudoku.size)
            self.fill_upload_field()
        self.mode = 'standard'
        self.all_cells = create_all_cells(16)
        self.cell_in_focus = (0, 0)
        self.playing_window = None
        set_up_sudoku_grid(self, 16)

        self.return_button.clicked.connect(self.return_to_main_window)
        self.upload_button.clicked.connect(lambda: self.notify_uploading(override=True))


class UploadChess9x9(UploadMaster, Ui_UploadWindow):
    """the window used to upload sudokus"""
    def __init__(self, sudoku: Sudoku|None = None):
        super().__init__()

        self.setupUi(self)
        if sudoku is None:
            self.sudoku_game = Sudoku(size = 9)
        else:
            self.sudoku_game = Sudoku(sudoku.originalgrid, sudoku.size)
            self.fill_upload_field()
        self.mode = 'chess'
        self.all_cells = create_all_cells(9)
        self.cell_in_focus = (0, 0)
        set_up_sudoku_grid(self, 9)

        self.return_button.clicked.connect(self.return_to_main_window)
        self.upload_button.clicked.connect(lambda: self.notify_uploading(mode=2))


class UploadChess4x4(UploadMaster, Ui_UploadWindow4x4):
    """the window used to upload sudokus"""
    def __init__(self, sudoku: Sudoku|None = None):
        super().__init__()
        self.setupUi(self)
        if sudoku is None:
            self.sudoku_game = Sudoku(size = 4)
        else:
            self.sudoku_game = Sudoku(sudoku.originalgrid, sudoku.size)
            self.fill_upload_field()
        self.mode = 'chess'
        self.all_cells = create_all_cells(4)
        self.cell_in_focus = (0, 0)
        self.playing_window = None
        set_up_sudoku_grid(self, 4)

        self.return_button.clicked.connect(self.return_to_main_window)
        self.upload_button.clicked.connect(lambda: self.notify_uploading(mode=2))


class UploadChess16x16(UploadMaster, Ui_UploadWindow16x16):
    """the window used to upload 16x16 sudokus"""
    def __init__(self, sudoku: Sudoku|None = None):
        super().__init__()
        self.setupUi(self)
        if sudoku is None:
            self.sudoku_game = Sudoku(size=16)
        else:
            self.sudoku_game = Sudoku(sudoku.originalgrid, sudoku.size)
            self.fill_upload_field()
        self.mode = 'chess'
        self.all_cells = create_all_cells(16)
        self.cell_in_focus = (0, 0)
        self.playing_window = None
        set_up_sudoku_grid(self, 16)

        self.return_button.clicked.connect(self.return_to_main_window)
        self.upload_button.clicked.connect(lambda: self.notify_uploading(mode=2, override=True))


class UploadDiagonal9x9(UploadMaster, Ui_UploadWindow):
    '''the window used to upload diagonal 9x9 sudokus'''
    def __init__(self, sudoku: Sudoku|None = None):
        super().__init__()

        self.setupUi(self)
        if sudoku is None:
            self.sudoku_game = Sudoku(size = 9)
        else:
            self.sudoku_game = Sudoku(sudoku.originalgrid, sudoku.size)
            self.fill_upload_field()
        self.mode = 'diagonal'
        self.all_cells = create_all_cells(9)
        self.cell_in_focus = (0, 0)
        set_up_sudoku_grid(self, 9)

        self.return_button.clicked.connect(self.return_to_main_window)
        self.upload_button.clicked.connect(lambda: self.notify_uploading(mode=1))


class UploadDiagonal4x4(UploadMaster, Ui_UploadWindow4x4):
    """the window used to upload diagonal 4x4 sudokus"""
    def __init__(self, sudoku: Sudoku|None = None):
        super().__init__()

        self.setupUi(self)
        if sudoku is None:
            self.sudoku_game = Sudoku(size = 4)
        else:
            self.sudoku_game = Sudoku(sudoku.originalgrid, sudoku.size)
            self.fill_upload_field()
        self.mode = 'diagonal'
        self.all_cells = create_all_cells(4)
        self.cell_in_focus = (0, 0)
        set_up_sudoku_grid(self, 4)

        self.return_button.clicked.connect(self.return_to_main_window)
        self.upload_button.clicked.connect(lambda: self.notify_uploading(mode=1))


class UploadDiagonal16x16(UploadMaster, Ui_UploadWindow16x16):
    '''the window used to upload diagonal 16x16 sudokus'''
    def __init__(self, sudoku: Sudoku|None = None):
        super().__init__()

        self.setupUi(self)
        if sudoku is None:
            self.sudoku_game = Sudoku(size = 16)
        else:
            self.sudoku_game = Sudoku(sudoku.originalgrid, sudoku.size)
            self.fill_upload_field()
        self.mode = 'diagonal'
        self.all_cells = create_all_cells(16)
        self.cell_in_focus = (0, 0)
        set_up_sudoku_grid(self, 16)

        self.return_button.clicked.connect(self.return_to_main_window)
        self.upload_button.clicked.connect(lambda: self.notify_uploading(mode=1, override=True))



class PlayingWindowMaster(qtw.QWidget):
    ''''This class contains many functions that are often used in the playing windows.
        Since the three different sizes have similar functions this is
        a parent class for the three sizes. We use the attributes of the children classes,
        which raises mypy [attr-defined] errors,
        so we sometimes need to ignore mypy errors related to these lines.'''

    def reset_hint_generator(self, variant):
        '''
        function called to (re)set the Hints object

        when a hint is called, the function also resets all involved grid cells to the right layout,
        i.e. transparency, focus_colour and bold numbers.
        '''

        self.lb_hint1.setText('')
        self.lb_hint2.setText('')
        self.basis = Basis(self.sudoku_game, variant)
        self.hints = Hints(self.basis)
        self.hidden_pairs = self.hints.hidden_pairs()
        self.hidden_singles = self.hints.hidden_singles()
        self.conjugate_pairs = self.hints.conjugatepairs()
        self.pointing_pairs = self.hints.pointing_pairs()
        self.box_line_red = self.hints.box_line_reduction()

    def reset_grid_layout(self):
        """Sets the layout of all the cells in the grid to what they should be.
            Depending on what number, if any, is entered in the grid"""
        for current_cell in self.all_cells:
            row = int(current_cell[6:])
            column = int(current_cell[3:5])
            if self.sudoku_game.originalgrid[row][column] != 0:
                getattr(self, current_cell).setReadOnly(True)
                if self.mode == 'diagonal' and (row == column or
                                                (row + column == self.sudoku_game.size - 1)):
                    getattr(self, current_cell).setStyleSheet("QLineEdit{\n"
                                                f'{self.font}'
                                                "background-color: rgb(230, 230, 230);\n"
                                                "}\n"
                                                "QLineEdit:focus {\n"
                                                "	background-color: rgb(163, 223, 249);\n"
                                                "}")
                else:
                    getattr(self, current_cell).setStyleSheet("QLineEdit{\n"
                                                f'{self.font}'
                                                "background-color: rgb(255, 255, 255);\n"
                                                "}\n"
                                                "QLineEdit:focus {\n"
                                                "	background-color: rgb(163, 223, 249);\n"
                                                "}")
            elif self.sudoku_game.editablegrid[row][column] != 0:
                if self.mode == 'diagonal' and (
                    row == column or (row + column == self.sudoku_game.size - 1)):
                    getattr(self, current_cell).setStyleSheet("QLineEdit{\n"
                                                        "background-color: rgb(230, 230, 230);\n"
                                                        "}\n"
                                                        "QLineEdit:focus {\n"
                                                        "	background-color: rgb(163, 223, 249);\n"
                                                        "}")
                else:
                    getattr(self, current_cell).setStyleSheet("QLineEdit{\n"
                                                        "background-color: rgb(255, 255, 255);\n"
                                                        "}\n"
                                                        "QLineEdit:focus {\n"
                                                        "	background-color: rgb(163, 223, 249);\n"
                                                        "}")
            else:
                if self.mode == 'diagonal' and (row == column or
                                                (row + column == self.sudoku_game.size - 1)):
                    getattr(self, current_cell).setStyleSheet("QLineEdit{\n"
                                                "background-color: rgba(203, 203, 203, 99);\n"
                                                "}\n"
                                                "QLineEdit:focus {\n"
                                                "	background-color: rgba(163, 223, 249, 99);\n"
                                                "}")
                else:
                    getattr(self, current_cell).setStyleSheet("QLineEdit{\n"
                                                "background-color: rgba(255, 255, 255, 0);\n"
                                                "}\n"
                                                "QLineEdit:focus {\n"
                                                "	background-color: rgba(163, 223, 249, 99);\n"
                                                "}")

    def cell_into_grid(self, number):
        """checks if a note should be added or a regular number"""
        if self.notes_mode == 'off':
            self.number_into_grid(number)
        else:
            self.number_into_note(int(number))

    def number_into_grid(self, number) -> None:
        """Stores the number entered by the user in the corresponding position
            in the editablegrid of the Sudoku class object. Unlike in the upload window,
            the originalgrid stays unchanged. The Hints object  is reset when a number
            is added or deleted.
        """
        column, row = self.cell_in_focus                    # type: ignore[attr-defined]
        string = index_to_cell(row, column)
        if number == '':
            self.sudoku_game.fillcooruser(0, row, column)   # type: ignore[attr-defined]
            getattr(self, string).setStyleSheet("QLineEdit{\n"
	                                            "background-color: rgba(255, 255, 255, 0);\n"
                                                "}\n"
                                                "QLineEdit:focus {\n"
                                                "	background-color: rgba(163, 223, 249, 99);\n"
                                                "}")
        else:
            if self.mode == 'diagonal' and (row == column or    # type: ignore[attr-defined]
                (row + column == self.sudoku_game.size - 1)):   # type: ignore[attr-defined]
                self.sudoku_game.fillcooruser(                  # type: ignore[attr-defined]
                                              int(number), row, column)
                getattr(self, string).setStyleSheet("QLineEdit{\n"
                                                    "background-color: rgba(203, 203, 203, 99);\n"
                                                    "}\n"
                                                    "QLineEdit:focus {\n"
                                                    "	background-color: rgba(163, 223, 249, 99);\n"
                                                    "}")
            else:
                self.sudoku_game.fillcooruser(int(number), row, column) # type: ignore[attr-defined]
                getattr(self, string).setStyleSheet("QLineEdit{\n"
                                                    "background-color: rgb(255, 255, 255);\n"
                                                    "}\n"
                                                    "QLineEdit:focus {\n"
                                                    "	background-color: rgb(163, 223, 249);\n"
                                                    "}")

        self.reset_grid_layout()
        self.reset_hint_generator(variant=self.mode)        # type: ignore[attr-defined]

        if (self.sudoku_game.editablegrid ==                # type: ignore[attr-defined]
            self.sudoku_game.solutiongrid):                 # type: ignore[attr-defined]
            self.we_have_a_winner()

    def number_into_note(self, number: int):
        """Turns the number entered by the user into a note, when self.notes_mode is on.
            removes the note if it is already present."""
        column, row = self.cell_in_focus                    # type: ignore[attr-defined]
        string = index_to_cell(row, column)
        getattr(self, string).setText('')
        edit_grid = self.sudoku_game.editablegrid           # type: ignore[attr-defined]
        if edit_grid[row][column].notes[number] == '  ':
            edit_grid[row][column].notes[number] = str(number)
        else:
            edit_grid[row][column].notes[number] = '  '

        n = edit_grid[row][column].notes.copy()
        notes_string = (f'  {n[1]}   {n[2]}   {n[3]}\n'
                        f'  {n[4]}   {n[5]}   {n[6]}\n'
                        f'  {n[7]}   {n[8]}   {n[9]}')

        cell_notes = index_to_note(row, column)
        getattr(self, cell_notes).setText(notes_string)

    def fill_playing_field(self, size):
        """turns the numbers entered on the upload screen permanent: so that they can't be
            changed accidentally"""

        for row in range(size):
            for column in range(size):
                number = self.sudoku_game.originalgrid[column][row]
                if number != 0:
                    if (self.mode == 'diagonal' and (row == column or (row + column == size - 1))):
                        string = index_to_cell(column, row)
                        getattr(self, string).setText(str(number))
                        getattr(self, string).setReadOnly(True)
                        getattr(self, string).setStyleSheet("QLineEdit{\n"
                                                f'{self.font}'
                                                "background-color: rgba(203, 203, 203, 99);\n"
                                                "}\n"
                                                "QLineEdit:focus {\n"
                                                "	background-color: rgba(163, 223, 249, 99);\n"
                                                "}")
                    else:
                        string = index_to_cell(column, row)
                        getattr(self, string).setText(str(number))
                        getattr(self, string).setReadOnly(True)
                        getattr(self, string).setStyleSheet(self.font)

    def show_hiddensingle(self):
        """output of hidden_pairs generator is a tuple in the form of:
        shape (row, column or block), number, tuple(row, column)

        When the hidden_pairs button is pressed the function first checks whether there is
        an error in the playing grid. If so a window is raised saying no hint is available.
        If not, the next output of the hidden_singles generator is called and the correct number
        is entered into the grid. The affected cell is highlighted in yellow.

        When the generator returns a StopIteration error, a window is raised indicating that this
        specific hint is not currently available."""

        if not self.sudoku_game.comparetoanswer()[0]:
            print('there is a mistake')
            self.no_hint_mistake = NoHintMistake()
            self.no_hint_mistake.show()
            return
        print('there is not a mistake')
        try:
            shape, number, self.hint_index = next(self.hidden_singles)
            print(self.hint_index)
            for index in self.hint_index:
                string = index_to_cell(index[0], index[1])
                getattr(self, string).setStyleSheet(u"QLineEdit{\n"
                                                    "background-color: rgb(255, 255, 127);\n"
                                                    f'{self.font}'
                                                    "}\n"
                                                    u"QLineEdit:focus {\n"
                                                    "	background-color: rgb(163, 223, 249);\n"
                                                    "}")

            self.lb_hint1.setText(f'Take a look at the yellow {shape}')
            self.lb_hint2.setText(f'The number {number} only has 1 possible spot')
        except StopIteration:
            self.not_available = NoHintAvailable()
            self.not_available.show()

    def show_hiddenpairs(self):
        """output of hidden_pairs generator is a list in the form of:
        [[row, column, number1, number2 ...], ...]

        When the hidden_pairs button is pressed the function first checks whether there
        is an error in the playing grid. If so a window is raised saying no hint is available.
        If not, the next output of the hidden_pairs generator is called and the correct numbers
        are entered as notes. The affected cells are highlighted in yellow.

        When the generator returns a StopIteration error, a window is raised indicating that this
        specific hint is not currently available.
        """
        if not self.sudoku_game.comparetoanswer()[0]:
            print('there is a mistake')
            self.no_hint_mistake = NoHintMistake()
            self.no_hint_mistake.show()
            return
        try:
            list_of_cells = next(self.hidden_pairs)
            self.reset_grid_layout()
            for cell in list_of_cells:
                row, column = cell[:2]
                self.sudoku_game.editablegrid[row][column].clearnotes()
                for number in cell[2:]:
                    self.sudoku_game.editablegrid[row][column].notes[number] = number

                n = self.sudoku_game.editablegrid[row][column].notes.copy()
                notes_string = (f'  {n[1]}   {n[2]}   {n[3]}\n'
                                f'  {n[4]}   {n[5]}   {n[6]}\n'
                                f'  {n[7]}   {n[8]}   {n[9]}')

                cell_notes = index_to_note(row, column)
                getattr(self, cell_notes).setText(notes_string)

                string = index_to_cell(row, column)
                getattr(self, string).setStyleSheet("QLineEdit{\n"
                                                    "background-color: rgba(255, 255, 127, 150);\n"
                                                    'font: 700 24pt "Segoe UI";'
                                                    "}\n"
                                                    "QLineEdit:focus {\n"
                                                    "	background-color: rgb(163, 223, 249);\n"
                                                    "}")
        except StopIteration:
            self.not_available = NoHintAvailable()
            self.not_available.show()

    def show_pointingpairs(self):
        """
        DESCRIPTION TAKEN FROM HINTS NOT FINAL
        Detects pointing pairs and triples according to sudoku wiki from a sudoku in this class.

        Returns:
        - an iterator of a tuple of 3 items: coordinates, the value and the sort of pair
        - coordinates: a list with row and column coordinates of the cell that needs to be adjusted
        - the value: the value that needs to be removed from the notes in the regarding cell
        - sort of pair: whether it is a pointing pair in column or row direction
        """
        if not self.sudoku_game.comparetoanswer()[0]:
            print('there is a mistake')
            self.no_hint_mistake = NoHintMistake()
            self.no_hint_mistake.show()
            return
        while True:
            try:
                new_hint = next(self.pointing_pairs)
                location, value, sort = new_hint[0], new_hint[1], new_hint[2]
                print(f'location is {location}\nvalue is {value}')
                row, column = location
                if self.sudoku_game.editablegrid[row][column].notes[value] == '  ':
                    print('there is no note there\n--------------------')
                else:
                    print('there is a note there\n-------------------------')
                    self.sudoku_game.editablegrid[row][column].notes[value] = '  '

                    n = self.sudoku_game.editablegrid[row][column].notes.copy()
                    print(n)
                    notes_string = (f'  {n[1]}   {n[2]}   {n[3]}\n'
                                    f'  {n[4]}   {n[5]}   {n[6]}\n'
                                    f'  {n[7]}   {n[8]}   {n[9]}')

                    cell_notes = index_to_note(row, column)
                    getattr(self, cell_notes).setText(notes_string)

                    string = index_to_cell(row, column)
                    getattr(self, string).setStyleSheet(
                                        u"QLineEdit{\n"
                                        "background-color: rgba(255, 255, 127, 150);\n"
                                        f'{self.font}'
                                        "}\n"
                                        u"QLineEdit:focus {\n"
                                        "	background-color: rgb(163, 223, 249);\n"
                                        "}")
                    self.reset_hint_generator(variant=self.mode)
                    self.lb_hint1.setText(f'{value} removed with pointing pairs')
                    self.lb_hint2.setText(f'check the {sort} to confirm')
                    break
            except StopIteration:
                self.not_available = NoHintAvailable()
                self.not_available.show()
                self.reset_hint_generator(variant=self.mode)
                break

    def show_box_line_red(self):
        if not self.sudoku_game.comparetoanswer()[0]:
            print('there is a mistake')
            self.no_hint_mistake = NoHintMistake()
            self.no_hint_mistake.show()
            return
        while True:
            try:
                new_hint = next(self.box_line_red)
                location, value = new_hint[0], new_hint[1]
                print(f'location is {location}\nvalue is {value}')
                row, column = location
                if self.sudoku_game.editablegrid[row][column].notes[value] == '  ':
                    print('there is no note there\n--------------------')
                    continue
                else:
                    print('there is a note there\n-------------------------')
                    self.sudoku_game.editablegrid[row][column].notes[value] = '  '

                    n = self.sudoku_game.editablegrid[row][column].notes.copy()
                    print(n)
                    notes_string = (f'  {n[1]}   {n[2]}   {n[3]}\n'
                                    f'  {n[4]}   {n[5]}   {n[6]}\n'
                                    f'  {n[7]}   {n[8]}   {n[9]}')

                    cell_notes = index_to_note(row, column)
                    getattr(self, cell_notes).setText(notes_string)

                    string = index_to_cell(row, column)
                    getattr(self, string).setStyleSheet(
                                        "QLineEdit{\n"
                                        "background-color: rgba(255, 255, 127, 150);\n"
                                        f'{self.font}'
                                        "}\n"
                                        "QLineEdit:focus {\n"
                                        "	background-color: rgb(163, 223, 249);\n"
                                        "}")
                    self.reset_hint_generator(variant=self.mode)
                    self.lb_hint1.setText(f'{value} removed with box/line')
                    self.lb_hint2.setText('reduction, check the box to confirm')
                    break
            except StopIteration:
                self.not_available = NoHintAvailable()
                self.not_available.show()
                self.reset_hint_generator(variant=self.mode)
                break

    def show_conjugatepairs(self):
        """output of hidden_pairs generator is a tuple in the form of:
        shape(row, column or block), type (double, triple, quad), list((row1, column1),
        (number1, number2, ...), ...)

        When the hidden_pairs button is pressed the function first checks whether there is
        an error in the playing grid. If so a window is raised saying no hint is available.
        If not, the next output of the conjugate_pairs generator is called and the correct
        numbers are entered as notes. The affected cells are highlighted in yellow.

        When the generator returns a StopIteration error, a window is raised indicating that 
        this specific hint is not currently available.
        """
        if not self.sudoku_game.comparetoanswer()[0]:
            print('there is a mistake')
            self.no_hint_mistake = NoHintMistake()
            self.no_hint_mistake.show()
            return
        try:
            list_of_cells = next(self.conjugate_pairs)[2]
            for cell in list_of_cells:
                row, column = cell[0]
                numbers = cell[1]
                self.sudoku_game.editablegrid[row][column].clearnotes()
                for number in numbers:
                    self.sudoku_game.editablegrid[row][column].notes[number] = number

                n = self.sudoku_game.editablegrid[row][column].notes.copy()
                notes_string = (f'  {n[1]}   {n[2]}   {n[3]}\n'
                                f'  {n[4]}   {n[5]}   {n[6]}\n'
                                f'  {n[7]}   {n[8]}   {n[9]}')

                cell_notes = index_to_note(row, column)
                getattr(self, cell_notes).setText(notes_string)

                string = index_to_cell(row, column)
                getattr(self, string).setStyleSheet("QLineEdit{\n"
                                                    "background-color: rgba(255, 255, 127, 150);\n"
                                                    'font: 700 24pt "Segoe UI";'
                                                    "}\n"
                                                    "QLineEdit:focus {\n"
                                                    "	background-color: rgb(163, 223, 249);\n"
                                                    "}")
        except StopIteration:
            self.not_available = NoHintAvailable()
            self.not_available.show()

    def toggle_solution(self):
        """Toggles the solution of the uploaded sudoku when the button is hit"""
        if self.solution_button.text() == 'Show Solution':
            for cell in self.all_cells:
                column = int(cell[3:5])
                row = int(cell[6:])
                solution_number = self.sudoku_game.solutiongrid[row][column]
                getattr(self, cell).setText(str(solution_number))
                getattr(self, cell).setReadOnly(True)
                if self.mode == 'diagonal' and (row == column or
                                                (row + column == self.sudoku_game.size - 1)):
                    getattr(self, cell).setStyleSheet("background-color: rgb(230, 230, 230);\n")
                else:
                    getattr(self, cell).setStyleSheet("background-color: rgb(255, 255, 255);")
            self.solution_button.setText('Hide Solution')
            self.solution_button.setStyleSheet("background-color: rgb(255, 0, 255);")
        else:
            for cell in self.all_cells:
                column = int(cell[3:5])
                row = int(cell[6:])
                editable_number = self.sudoku_game.editablegrid[row][column]
                getattr(self, cell).setReadOnly(False)
                if editable_number == 0:
                    getattr(self, cell).setText('')
                else:
                    getattr(self, cell).setText(str(editable_number))
            self.solution_button.setText('Show Solution')
            self.solution_button.setStyleSheet("background-color: rgb(28, 206, 255);")
            self.reset_grid_layout()

    def toggle_notes(self):
        """toggles the notes_mode attribute. Furthermore, ensures that cells that have been
            filled in can't be interacted with when notes_mode is turned on.
            restores back to the original grid settings when notes_mode
            is turned off."""
        if self.notes_button.text() == 'Notes\nOff':
            self.notes_mode = 'on'
            self.notes_button.setText('Notes\nOn')
            self.notes_button.setStyleSheet('background-color: rgb(11, 182, 229);')
            for row in range(self.sudoku_game.size):
                for column in range(self.sudoku_game.size):
                    if self.sudoku_game.editablegrid[row][column] != 0:
                        string = index_to_cell(row, column)
                        getattr(self, string).setReadOnly(True)

        else:
            self.notes_mode = 'off'
            self.notes_button.setText('Notes\nOff')
            self.notes_button.setStyleSheet('background-color: rgb(182, 182, 182);')
            for row in range(self.sudoku_game.size):
                for column in range(self.sudoku_game.size):
                    string = index_to_cell(row, column)
                    if self.solution_button.text() == 'Hide Solution':
                        getattr(self, string).setReadOnly(True)
                    else:
                        getattr(self, string).setReadOnly(False)
                        if self.sudoku_game.originalgrid[row][column] != 0:
                            getattr(self, string).setReadOnly(True)
                        if self.solution_button.text() == 'Hide Solution':
                            getattr(self, string).setReadOnly(True)


    def any_mistakes(self):
        """when the button is hit, all cells in the editablegrid are compared to the solutiongrid.
            If there is a discrepancy, the error count is raised by 1 and the incorrect cell
            is added to the incorrect cells attribute.

            The amount of mistakes is shown to the user in the UI. If there is any mistakes the
            'show mistakes'-button is revealed."""
        count = 0
        self.incorrect_cells = []
        if not self.sudoku_game.comparetoanswer()[0]:
            for row in range(self.sudoku_game.size):
                for column in range(self.sudoku_game.size):
                    if (self.sudoku_game.editablegrid[row][column] != 0 and
                        (self.sudoku_game.editablegrid[row][column] !=
                         self.sudoku_game.solutiongrid[row][column])):
                        count += 1
                        incorrect = index_to_cell(row, column)
                        self.incorrect_cells.append(incorrect)

        if count == 0:
            self.lb_hint2.setText('      You currently have no mistakes!')
        elif count == 1:
            self.lb_hint2.setText(f'        You currently have {count} mistake!')
            self.show_mistakes_button.show()
        else:
            self.lb_hint2.setText(f'        You currently have {count} mistakes!')
            self.show_mistakes_button.show()

    def show_mistakes(self):
        """colors the incorrect cells red when button is pressed"""
        for cell in self.incorrect_cells:
            getattr(self, cell).setStyleSheet('background-color: rgb(255, 30, 30);')
        self.show_mistakes_button.hide()

    def we_have_a_winner(self):
        """function that is called when sudoku.editablegrid == sudoku.solutiongrid"""
        self.winner = Winner()
        self.winner.show()

    def show_info(self):
        """Provides information about solving sudokus"""
        self.info = Information()
        self.info.setAttribute(Qt.WA_DeleteOnClose)
        self.info.show()

    def return_to_main_window(self):
        """opens up a confirmation screen if the user wishes to return to the main window"""
        self.confirm = ConfirmToMain(self)
        self.confirm.setAttribute(Qt.WA_DeleteOnClose)
        self.confirm.show()

class PlayingWindow9x9(PlayingWindowMaster, Ui_PlayingWindow):
    """The window used to play the uploaded sudoku game.
        This is also the window where a user can ask for hints."""

    def __init__(self, uploaded_sudoku):
        super().__init__()
        self.setupUi(self)
        self.show_mistakes_button.hide()
        self.all_cells = create_all_cells(9)
        self.all_notes = create_all_notes(9, self)
        self.cell_in_focus = (0, 0)    #index 0 = column, index 1 = row
        self.mode = 'standard'
        self.incorrect_cells = []
        self.hint_index = None
        self.notes_mode = 'off'
        self.font = 'font: 700 24pt "Segoe UI";'
        self.upload_window: Upload9x9


        set_up_sudoku_grid(self, 9)
        self.sudoku_game = uploaded_sudoku
        self.reset_hint_generator(variant=self.mode)

        self.help_button.clicked.connect(self.show_hiddensingle)
        self.hidden_pairs_button.clicked.connect(self.show_hiddenpairs)
        self.naked_pairs_button.clicked.connect(self.show_conjugatepairs)
        self.pointing_pairs_button.clicked.connect(self.show_pointingpairs)
        self.box_line_red_button.clicked.connect(self.show_box_line_red)
        self.return_button.clicked.connect(self.return_to_main_window)
        self.return_upload_button.clicked.connect(self.return_upload_window)
        self.solution_button.clicked.connect(self.toggle_solution)
        self.notes_button.clicked.connect(self.toggle_notes)
        self.any_mistakes_button.clicked.connect(self.any_mistakes)
        self.show_mistakes_button.clicked.connect(self.show_mistakes)
        self.info_button.clicked.connect(self.show_info)
        self.fill_playing_field(9)

    def return_upload_window(self):
        """returns the user to the upload window to alter the originalgrid."""
        self.upload_window = Upload9x9(self.sudoku_game)
        self.upload_window.setAttribute(Qt.WA_DeleteOnClose)
        self.upload_window.show()
        self.close()

class PlayingWindow4x4(PlayingWindowMaster, Ui_PlayingWindow4x4):
    """The window used to play the uploaded sudoku game.
        This is also the window where a user can ask for hints."""

    def __init__(self, uploaded_sudoku):
        super().__init__()

        self.setupUi(self)
        self.show_mistakes_button.hide()
        self.all_cells = create_all_cells(4)
        self.all_notes = create_all_notes(4, self)
        self.cell_in_focus = (0, 0)    #index 0 = column, index 1 = row
        self.mode = 'standard'
        self.incorrect_cells = []
        self.hint_index = None
        self.notes_mode = 'off'
        self.font = 'font: 700 50pt "Segoe UI";'
        self.upload_window: Upload4x4


        set_up_sudoku_grid(self, 4)
        self.sudoku_game = uploaded_sudoku
        self.reset_hint_generator(variant=self.mode)

        self.help_button.clicked.connect(self.show_hiddensingle)
        self.return_button.clicked.connect(self.return_to_main_window)
        self.return_upload_button.clicked.connect(self.return_upload_window)
        self.solution_button.clicked.connect(self.toggle_solution)
        self.notes_button.clicked.connect(self.toggle_notes)
        self.any_mistakes_button.clicked.connect(self.any_mistakes)
        self.show_mistakes_button.clicked.connect(self.show_mistakes)
        self.info_button.clicked.connect(self.show_info)
        self.fill_playing_field(4)

    def return_upload_window(self):
        """returns the user to the upload window to alter the originalgrid."""
        self.upload_window = Upload4x4(self.sudoku_game)
        self.upload_window.setAttribute(Qt.WA_DeleteOnClose)
        self.upload_window.show()
        self.close()

class PlayingWindow16x16(PlayingWindowMaster, Ui_PlayingWindow16x16):
    """The window used to play the uploaded sudoku game.
        This is also the window where a user can ask for hints."""

    def __init__(self, uploaded_sudoku):
        super().__init__()

        self.setupUi(self)
        self.show_mistakes_button.hide()
        self.all_cells = create_all_cells(16)
        self.cell_in_focus = (0, 0)    #index 0 = column, index 1 = row
        self.mode = 'standard'
        self.incorrect_cells = []
        self.hint_index = None
        self.font = 'font: 700 16pt "Segoe UI";'
        self.upload_window: Upload16x16


        set_up_sudoku_grid(self, 16)
        self.sudoku_game = uploaded_sudoku
        self.reset_hint_generator(variant=self.mode)

        self.help_button.clicked.connect(self.show_hiddensingle)
        self.return_button.clicked.connect(self.return_to_main_window)
        self.return_upload_button.clicked.connect(self.return_upload_window)
        self.solution_button.clicked.connect(self.toggle_solution)
        self.any_mistakes_button.clicked.connect(self.any_mistakes)
        self.show_mistakes_button.clicked.connect(self.show_mistakes)
        self.info_button.clicked.connect(self.show_info)
        self.fill_playing_field(16)

    def cell_into_grid(self, number) -> None:
        self.number_into_grid(number)

    def return_upload_window(self):
        """returns the user to the upload window to alter the originalgrid."""
        self.upload_window = Upload16x16(self.sudoku_game)
        self.upload_window.setAttribute(Qt.WA_DeleteOnClose)
        self.upload_window.show()
        self.close()

class PlayingWindowDiagonal9x9(PlayingWindowMaster, Ui_PlayingWindow):
    """The window used to play the uploaded sudoku game.
        This is also the window where a user can ask for hints."""

    def __init__(self, uploaded_sudoku):
        super().__init__()
        self.setupUi(self)
        self.show_mistakes_button.hide()
        self.all_cells = create_all_cells(9)
        self.all_notes = create_all_notes(9, self)
        self.cell_in_focus = (0, 0)    #index 0 = column, index 1 = row
        self.mode = 'diagonal'
        self.incorrect_cells = []
        self.hint_index = None
        self.notes_mode = 'off'
        self.font = 'font: 700 24pt "Segoe UI";'
        self.upload_window: UploadDiagonal9x9


        set_up_sudoku_grid(self, 9)
        self.sudoku_game = uploaded_sudoku
        self.reset_hint_generator(variant=self.mode)

        self.help_button.clicked.connect(self.show_hiddensingle)
        self.hidden_pairs_button.clicked.connect(self.show_hiddenpairs)
        self.naked_pairs_button.clicked.connect(self.show_conjugatepairs)
        self.pointing_pairs_button.clicked.connect(self.show_pointingpairs)
        self.box_line_red_button.clicked.connect(self.show_box_line_red)
        self.return_button.clicked.connect(self.return_to_main_window)
        self.return_upload_button.clicked.connect(self.return_upload_window)
        self.solution_button.clicked.connect(self.toggle_solution)
        self.notes_button.clicked.connect(self.toggle_notes)
        self.any_mistakes_button.clicked.connect(self.any_mistakes)
        self.show_mistakes_button.clicked.connect(self.show_mistakes)
        self.info_button.clicked.connect(self.show_info)
        self.fill_playing_field(9)

    def return_upload_window(self):
        """returns the user to the upload window to alter the originalgrid."""
        self.upload_window = UploadDiagonal9x9(self.sudoku_game)
        self.upload_window.setAttribute(Qt.WA_DeleteOnClose)
        self.upload_window.show()
        self.close()


class PlayingWindowChess9x9(PlayingWindowMaster, Ui_PlayingWindow):
    """The window used to play the uploaded sudoku game.
        This is also the window where a user can ask for hints."""

    def __init__(self, uploaded_sudoku):
        super().__init__()
        self.setupUi(self)
        self.show_mistakes_button.hide()
        self.all_cells = create_all_cells(9)
        self.all_notes = create_all_notes(9, self)
        self.cell_in_focus = (0, 0)    #index 0 = column, index 1 = row
        self.mode = 'chess'
        self.incorrect_cells = []
        self.hint_index = None
        self.notes_mode = 'off'
        self.font = 'font: 700 24pt "Segoe UI";'
        self.upload_window: UploadChess9x9


        set_up_sudoku_grid(self, 9)
        self.sudoku_game = uploaded_sudoku
        self.reset_hint_generator(variant=self.mode)

        self.help_button.clicked.connect(self.show_hiddensingle)
        self.hidden_pairs_button.clicked.connect(self.show_hiddenpairs)
        self.naked_pairs_button.clicked.connect(self.show_conjugatepairs)
        self.pointing_pairs_button.clicked.connect(self.show_pointingpairs)
        self.box_line_red_button.clicked.connect(self.show_box_line_red)
        self.return_button.clicked.connect(self.return_to_main_window)
        self.return_upload_button.clicked.connect(self.return_upload_window)
        self.solution_button.clicked.connect(self.toggle_solution)
        self.notes_button.clicked.connect(self.toggle_notes)
        self.any_mistakes_button.clicked.connect(self.any_mistakes)
        self.show_mistakes_button.clicked.connect(self.show_mistakes)
        self.info_button.clicked.connect(self.show_info)
        self.fill_playing_field(9)

    def return_upload_window(self):
        """returns the user to the upload window to alter the originalgrid."""
        self.upload_window = UploadChess9x9(self.sudoku_game)
        self.upload_window.setAttribute(Qt.WA_DeleteOnClose)
        self.upload_window.show()
        self.close()


class PlayingWindowChess4x4(PlayingWindowMaster, Ui_PlayingWindow4x4):
    """The window used to play the uploaded sudoku game.
        This is also the window where a user can ask for hints."""

    def __init__(self, uploaded_sudoku):
        super().__init__()
        self.setupUi(self)
        self.show_mistakes_button.hide()
        self.all_cells = create_all_cells(4)
        self.all_notes = create_all_notes(4, self)
        self.cell_in_focus = (0, 0)    #index 0 = column, index 1 = row
        self.mode = 'chess'
        self.incorrect_cells = []
        self.hint_index = None
        self.notes_mode = 'off'
        self.font = 'font: 700 24pt "Segoe UI";'
        self.upload_window: UploadChess4x4


        set_up_sudoku_grid(self, 4)
        self.sudoku_game = uploaded_sudoku
        self.reset_hint_generator(variant=self.mode)

        self.help_button.clicked.connect(self.show_hiddensingle)
        self.return_button.clicked.connect(self.return_to_main_window)
        self.return_upload_button.clicked.connect(self.return_upload_window)
        self.solution_button.clicked.connect(self.toggle_solution)
        self.notes_button.clicked.connect(self.toggle_notes)
        self.any_mistakes_button.clicked.connect(self.any_mistakes)
        self.show_mistakes_button.clicked.connect(self.show_mistakes)
        self.info_button.clicked.connect(self.show_info)
        self.fill_playing_field(4)

    def return_upload_window(self):
        """returns the user to the upload window to alter the originalgrid."""
        self.upload_window = UploadChess4x4(self.sudoku_game)
        self.upload_window.setAttribute(Qt.WA_DeleteOnClose)
        self.upload_window.show()
        self.close()


class PlayingWindowChess16x16(PlayingWindowMaster, Ui_PlayingWindow16x16):
    """The window used to play the uploaded sudoku game.
        This is also the window where a user can ask for hints."""

    def __init__(self, uploaded_sudoku):
        super().__init__()
        self.setupUi(self)
        self.show_mistakes_button.hide()
        self.all_cells = create_all_cells(16)
        self.cell_in_focus = (0, 0)    #index 0 = column, index 1 = row
        self.mode = 'chess'
        self.incorrect_cells = []
        self.hint_index = None
        self.notes_mode = 'off'
        self.font = 'font: 700 24pt "Segoe UI";'
        self.upload_window: UploadChess16x16


        set_up_sudoku_grid(self, 16)
        self.sudoku_game = uploaded_sudoku
        self.reset_hint_generator(variant=self.mode)

        self.help_button.clicked.connect(self.show_hiddensingle)
        self.hidden_pairs_button.clicked.connect(self.show_hiddenpairs)
        self.return_button.clicked.connect(self.return_to_main_window)
        self.return_upload_button.clicked.connect(self.return_upload_window)
        self.solution_button.clicked.connect(self.toggle_solution)
        self.notes_button.clicked.connect(self.toggle_notes)
        self.any_mistakes_button.clicked.connect(self.any_mistakes)
        self.show_mistakes_button.clicked.connect(self.show_mistakes)
        self.info_button.clicked.connect(self.show_info)
        self.fill_playing_field(16)

    def return_upload_window(self):
        """returns the user to the upload window to alter the originalgrid."""
        self.upload_window = UploadChess16x16(self.sudoku_game)
        self.upload_window.setAttribute(Qt.WA_DeleteOnClose)
        self.upload_window.show()
        self.close()


class PlayingWindowDiagonal4x4(PlayingWindowMaster, Ui_PlayingWindow4x4):
    """The window used to play the uploaded sudoku game.
        This is also the window where a user can ask for hints."""

    def __init__(self, uploaded_sudoku):
        super().__init__()
        self.setupUi(self)
        self.show_mistakes_button.hide()
        self.all_cells = create_all_cells(4)
        self.all_notes = create_all_notes(4, self)
        self.cell_in_focus = (0, 0)    #index 0 = column, index 1 = row
        self.mode = 'diagonal'
        self.incorrect_cells = []
        self.hint_index = None
        self.notes_mode = 'off'
        self.font = 'font: 700 50pt "Segoe UI";'
        self.upload_window: UploadDiagonal4x4


        set_up_sudoku_grid(self, 4)
        self.sudoku_game = uploaded_sudoku
        self.reset_hint_generator(variant=self.mode)

        self.help_button.clicked.connect(self.show_hiddensingle)
        self.return_button.clicked.connect(self.return_to_main_window)
        self.return_upload_button.clicked.connect(self.return_upload_window)
        self.solution_button.clicked.connect(self.toggle_solution)
        self.notes_button.clicked.connect(self.toggle_notes)
        self.any_mistakes_button.clicked.connect(self.any_mistakes)
        self.show_mistakes_button.clicked.connect(self.show_mistakes)
        self.info_button.clicked.connect(self.show_info)
        self.fill_playing_field(4)

    def return_upload_window(self):
        """returns the user to the upload window to alter the originalgrid."""
        self.upload_window = UploadDiagonal4x4(self.sudoku_game)
        self.upload_window.setAttribute(Qt.WA_DeleteOnClose)
        self.upload_window.show()
        self.close()

class PlayingWindowDiagonal16x16(PlayingWindowMaster, Ui_PlayingWindow16x16):
    """The window used to play the uploaded sudoku game.
        This is also the window where a user can ask for hints."""

    def __init__(self, uploaded_sudoku):
        super().__init__()
        self.setupUi(self)
        self.show_mistakes_button.hide()
        self.all_cells = create_all_cells(16)
        self.all_notes = create_all_notes(16, self)
        self.cell_in_focus = (0, 0)    #index 0 = column, index 1 = row
        self.mode = 'diagonal'
        self.incorrect_cells = []
        self.hint_index = None
        self.notes_mode = 'off'
        self.font = 'font: 700 16pt "Segoe UI";'
        self.upload_window: UploadDiagonal16x16


        set_up_sudoku_grid(self, 16)
        self.sudoku_game = uploaded_sudoku
        self.reset_hint_generator(variant=self.mode)

        self.help_button.clicked.connect(self.show_hiddensingle)
        self.hidden_pairs_button.clicked.connect(self.show_hiddenpairs)
        self.return_button.clicked.connect(self.return_to_main_window)
        self.return_upload_button.clicked.connect(self.return_upload_window)
        self.solution_button.clicked.connect(self.toggle_solution)
        self.notes_button.clicked.connect(self.toggle_notes)
        self.any_mistakes_button.clicked.connect(self.any_mistakes)
        self.show_mistakes_button.clicked.connect(self.show_mistakes)
        self.info_button.clicked.connect(self.show_info)
        self.fill_playing_field(16)

    def return_upload_window(self):
        """returns the user to the upload window to alter the originalgrid."""
        self.upload_window = UploadDiagonal16x16(self.sudoku_game)
        self.upload_window.setAttribute(Qt.WA_DeleteOnClose)
        self.upload_window.show()
        self.close()

class ConfirmToMain(qtw.QWidget, Ui_ConfirmToMain):
    """pop-up confirmation window if the user wishes to go the main screen"""

    def __init__(self, window):
        super().__init__()
        self.setupUi(self)

        self.ok_button.clicked.connect(lambda text: self.ok_clicked(window))
        self.cancel_button.clicked.connect(self.cancel_clicked)

    def ok_clicked(self, window):
        """Takes the user back to the main screen, when button is hit. Current sudoku is deleted"""
        window1.show()
        window.close()
        self.close()
        del window

    def cancel_clicked(self):
        """Takes the user back to the sudoku screen, when button is hit."""
        self.close()

class Winner(qtw.QWidget, Ui_WinnerWindow):
    """A window that is opened once you complete the sudoku"""

    def __init__(self):
        super().__init__()
        self.setupUi(self)

class SizeSelection(qtw.QWidget, Ui_SelectionScreen):
    """A window where you can select what size sudoku you want to upload"""

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.return_main.clicked.connect(self.return_to_main_window)
        self.Pb_9x9.clicked.connect(lambda: self.mode_checker(9))
        self.Pb_16x16.clicked.connect(lambda: self.mode_checker(16))
        self.Pb_4x4.clicked.connect(lambda: self.mode_checker(4))
        self.upload_window: (
            Upload9x9 | Upload4x4 | Upload16x16 |
            UploadDiagonal9x9 | UploadDiagonal4x4 | UploadDiagonal16x16 |
            UploadChess9x9 | UploadChess4x4 | UploadChess16x16)

    def mode_checker(self, selected_size: int):
        '''opens the correct playing window based on the mode selected in the dropmenu
            and the size selected with the buttons'''
        selected_mode = self.comboBox.currentText()
        if selected_mode == 'Standard':
            if selected_size == 9:
                self.open_upload_window(Upload9x9())
            elif selected_size == 4:
                self.open_upload_window(Upload4x4())
            else:
                self.open_upload_window(Upload16x16())
        elif selected_mode == 'Diagonal':
            if selected_size == 9:
                self.open_upload_window(UploadDiagonal9x9())
            elif selected_size == 4:
                self.open_upload_window(UploadDiagonal4x4())
            else:
                self.open_upload_window(UploadDiagonal16x16())
        elif selected_mode == 'Chess':
            if selected_size == 9:
                self.open_upload_window(UploadChess9x9())
            elif selected_size == 4:
                self.open_upload_window(UploadChess4x4())
            else:
                self.open_upload_window(UploadChess16x16())

    def open_upload_window(self, window_class):
        """opens up the specified upload window"""
        self.upload_window = window_class
        self.upload_window.setAttribute(Qt.WA_DeleteOnClose)
        self.upload_window.show()
        self.close()

    def return_to_main_window(self):
        """returns the user back to the main window"""
        window1.show()
        self.close()

class SizeSelectionGenerator(qtw.QWidget, Ui_SelectionScreenGenerator):
    """window where user can select the size of sudoku to be generated"""

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.wait_label.hide()
        self.Pb_4x4.clicked.connect(lambda: self.indicator(4))
        self.Pb_9x9.clicked.connect(lambda: self.indicator(9))
        self.return_main.clicked.connect(self.return_to_main_window)
        self.playing_window: PlayingWindow4x4 | PlayingWindow9x9
        self.sudoku_game: Sudoku

    @staticmethod
    def difficulty(lst):
        '''Returns the number of nonzero values in a sudoku (in list form)'''
        nonzero = 0
        for row in enumerate(lst):
            for col in enumerate(lst):
                if lst[row[0]][col[0]] != 0:
                    nonzero += 1
        return nonzero


    def indicator(self, size):
        """An interim function that indicates the user that the program is generating the sudoku.
        The open_playing_window function is opened after a short delay. The delay is necessary for
        the indication to become visible."""
        self.wait_label.show()
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.setSingleShot(True)
        self.timer.start()
        if size == 4:
            self.timer.timeout.connect(self.generate_4x4_sudoku)
        else:
            self.timer.timeout.connect(self.generate_9x9_sudoku)

    def generate_4x4_sudoku(self):
        """generates 4x4 sudoku and opens playing window"""
        start_time = time.time()
        time_limit = 15
        sudoku_list = []
        iteration = 0
        while time.time() < start_time + time_limit:
            gen = Generator(Sudoku(size=4), initial_values=2)
            sudoku_list.append(Sudoku(gen.generate_sudoku(), size=4))
            iteration += 1
        difficulty_list = [self.difficulty(sudoku.originalgrid) for sudoku in sudoku_list]
        if self.comboBox.currentText() == 'easy':
            self.sudoku_game = sudoku_list[difficulty_list.index(max(difficulty_list))]
        elif self.comboBox.currentText() == 'normal':
            sorted_difficulty = sorted(difficulty_list)
            middle_value = sorted_difficulty[len(sorted_difficulty) // 2]
            self.sudoku_game = sudoku_list[difficulty_list.index(middle_value)]
        else:
            self.sudoku_game = sudoku_list[difficulty_list.index(min(difficulty_list))]
        solver = Solver(self.sudoku_game)
        solver.solvebrute()
        self.playing_window = PlayingWindow4x4(self.sudoku_game)
        self.playing_window.return_upload_button.hide()
        self.playing_window.setAttribute(Qt.WA_DeleteOnClose)
        self.playing_window.show()
        self.close()

    def generate_9x9_sudoku(self):
        """generates 9x9 sudoku and opens playing window"""
        start_time = time.time()
        time_limit = 15
        sudoku_list = []
        iteration = 0
        while time.time() < start_time + time_limit:
            if iteration < 1:
                gen = Generator(Sudoku(size=9), initial_values=5)
            elif iteration < 4:
                gen = Generator(Sudoku(size=9), initial_values=10)
            else:
                break
            sudoku_list.append(Sudoku(gen.quick_find_sudoku()))
            iteration += 1
        difficulty_list = [self.difficulty(sudoku.originalgrid) for sudoku in sudoku_list]
        if self.comboBox.currentText() == 'easy':
            self.sudoku_game = sudoku_list[difficulty_list.index(max(difficulty_list))]
        elif self.comboBox.currentText() == 'normal':
            sorted_difficulty = sorted(difficulty_list)
            middle_value = sorted_difficulty[len(sorted_difficulty) // 2]
            self.sudoku_game = sudoku_list[difficulty_list.index(middle_value)]
        else:
            self.sudoku_game = sudoku_list[difficulty_list.index(min(difficulty_list))]
        solver = Solver(self.sudoku_game)
        solver.solvebrute()
        self.playing_window = PlayingWindow9x9(self.sudoku_game)
        self.playing_window.return_upload_button.hide()
        self.playing_window.setAttribute(Qt.WA_DeleteOnClose)
        self.playing_window.show()
        self.close()

    def return_to_main_window(self):
        """returns the user back to the main window"""
        window1.show()
        self.close()

class NotSolvable(qtw.QWidget, Ui_IncorrectSolution):
    """window that is opened when the uploaded sudoku is unsolvable"""

    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.pushButton.clicked.connect(self.close)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

class NotUnique(UploadMaster, Ui_SeveralSolution):
    """window that is opened when the uploaded sudoku is not unique, mypy raises an attr-defined
        error but it should not (and it doesn't for NotSolvable). Since the code works an ignore
        statement is added.
        """

    def __init__(self, open_window, sudoku_game, mode: int = 0):
        super().__init__()
        self.mode = mode
        self.sudoku_game = sudoku_game
        self.open_window = open_window
        self.setupUi(self)
        self.return_button.clicked.connect(self.close)
        self.continue_button.clicked.connect(self.continue_anyway)
        self.setWindowFlags(
            self.windowFlags() | Qt.FramelessWindowHint)    # type: ignore[attr-defined]

    def continue_anyway(self):
        """opens the playingwindow without having a unique solution"""
        self.open_playing_window(mode=self.mode, override=True)
        self.open_window.close()

class Information(qtw.QWidget, Ui_Information):
    """Shows the information screen, explaining the rules and the
        different algorithms used in the hint finder"""

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        image_path1 = os.path.join(os.path.dirname(__file__),
                                    'UI_sudoku', 'picture sudoku grid.png')
        image_path2 = os.path.join(os.path.dirname(__file__),
                                    'UI_sudoku', 'hidden single.png')

        self.label_13.setPixmap(QPixmap(image_path2))
        self.label_7.setPixmap(QPixmap(image_path1))



class NoHintMistake(qtw.QWidget, Ui_no_hint_mistake):
    """window that is opened if the user requests a hint when having an error in the sudoku grid"""

    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.pushButton.clicked.connect(self.close)
        self.setAttribute(Qt.WA_DeleteOnClose)

class NoHintAvailable(qtw.QWidget, Ui_no_hint_available):
    """window that is opened if the user requests a hint that is not
        available with the current sudoku grid"""

    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.pushButton.clicked.connect(self.close)
        self.setAttribute(Qt.WA_DeleteOnClose)



if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)

    window1 = MainWindow()

    sys.exit(app.exec())
