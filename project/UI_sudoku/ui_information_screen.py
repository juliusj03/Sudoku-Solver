# -*- coding: utf-8 -*-
# pylint: skip-file

################################################################################
## Form generated from reading UI file 'information_screenkNhcit.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QScrollArea,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Information(object):
    def setupUi(self, Information):
        if not Information.objectName():
            Information.setObjectName(u"Information")
        Information.resize(634, 625)
        Information.setMaximumSize(QSize(1600000, 1600000))
        Information.setStyleSheet(u"background-color: rgb(20, 114, 255);")
        self.verticalLayout = QVBoxLayout(Information)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = QScrollArea(Information)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setStyleSheet(u"background-color: rgb(20, 114, 255);")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 597, 2527))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame = QFrame(self.scrollAreaWidgetContents)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"background-color: rgb(83, 201, 255);")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_10 = QLabel(self.frame)
        self.label_10.setObjectName(u"label_10")
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_10.setFont(font)

        self.verticalLayout_3.addWidget(self.label_10)

        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_3.addWidget(self.label_3)

        self.label_11 = QLabel(self.frame)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font)

        self.verticalLayout_3.addWidget(self.label_11)

        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")
        font1 = QFont()
        font1.setBold(False)
        self.label_4.setFont(font1)

        self.verticalLayout_3.addWidget(self.label_4)

        self.label_7 = QLabel(self.frame)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setPixmap(QPixmap(u"../../../../Documents/MST/Minor Computer science/Computer Science Project/picture sudoku grid.png"))
        self.label_7.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_7)

        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")

        self.verticalLayout_3.addWidget(self.label)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.label_5 = QLabel(self.frame)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)

        self.verticalLayout_3.addWidget(self.label_5)

        self.label_6 = QLabel(self.frame)
        self.label_6.setObjectName(u"label_6")
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(True)
        self.label_6.setFont(font2)

        self.verticalLayout_3.addWidget(self.label_6)

        self.label_8 = QLabel(self.frame)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_3.addWidget(self.label_8)

        self.label_9 = QLabel(self.frame)
        self.label_9.setObjectName(u"label_9")

        self.verticalLayout_3.addWidget(self.label_9)

        self.label_12 = QLabel(self.frame)
        self.label_12.setObjectName(u"label_12")

        self.verticalLayout_3.addWidget(self.label_12)

        self.label_13 = QLabel(self.frame)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setPixmap(QPixmap(u"../../../../Documents/MST/Minor Computer science/Computer Science Project/hidden single.png"))
        self.label_13.setScaledContents(False)
        self.label_13.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_13)

        self.label_14 = QLabel(self.frame)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setFont(font2)

        self.verticalLayout_3.addWidget(self.label_14)

        self.label_15 = QLabel(self.frame)
        self.label_15.setObjectName(u"label_15")

        self.verticalLayout_3.addWidget(self.label_15)

        self.label_24 = QLabel(self.frame)
        self.label_24.setObjectName(u"label_24")
        font3 = QFont()
        font3.setBold(True)
        self.label_24.setFont(font3)

        self.verticalLayout_3.addWidget(self.label_24)

        self.label_25 = QLabel(self.frame)
        self.label_25.setObjectName(u"label_25")

        self.verticalLayout_3.addWidget(self.label_25)

        self.label_26 = QLabel(self.frame)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setFont(font3)

        self.verticalLayout_3.addWidget(self.label_26)

        self.label_27 = QLabel(self.frame)
        self.label_27.setObjectName(u"label_27")

        self.verticalLayout_3.addWidget(self.label_27)

        self.label_28 = QLabel(self.frame)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setFont(font3)

        self.verticalLayout_3.addWidget(self.label_28)

        self.label_29 = QLabel(self.frame)
        self.label_29.setObjectName(u"label_29")

        self.verticalLayout_3.addWidget(self.label_29)

        self.label_16 = QLabel(self.frame)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setFont(font2)

        self.verticalLayout_3.addWidget(self.label_16)

        self.label_17 = QLabel(self.frame)
        self.label_17.setObjectName(u"label_17")

        self.verticalLayout_3.addWidget(self.label_17)

        self.label_18 = QLabel(self.frame)
        self.label_18.setObjectName(u"label_18")
        font4 = QFont()
        font4.setPointSize(9)
        font4.setBold(True)
        self.label_18.setFont(font4)

        self.verticalLayout_3.addWidget(self.label_18)

        self.label_19 = QLabel(self.frame)
        self.label_19.setObjectName(u"label_19")

        self.verticalLayout_3.addWidget(self.label_19)

        self.label_20 = QLabel(self.frame)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setFont(font3)

        self.verticalLayout_3.addWidget(self.label_20)

        self.label_21 = QLabel(self.frame)
        self.label_21.setObjectName(u"label_21")

        self.verticalLayout_3.addWidget(self.label_21)

        self.label_22 = QLabel(self.frame)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setFont(font3)

        self.verticalLayout_3.addWidget(self.label_22)

        self.label_23 = QLabel(self.frame)
        self.label_23.setObjectName(u"label_23")

        self.verticalLayout_3.addWidget(self.label_23)

        self.label_30 = QLabel(self.frame)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setFont(font2)

        self.verticalLayout_3.addWidget(self.label_30)

        self.label_31 = QLabel(self.frame)
        self.label_31.setObjectName(u"label_31")

        self.verticalLayout_3.addWidget(self.label_31)

        self.label_32 = QLabel(self.frame)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setFont(font2)

        self.verticalLayout_3.addWidget(self.label_32)

        self.label_33 = QLabel(self.frame)
        self.label_33.setObjectName(u"label_33")

        self.verticalLayout_3.addWidget(self.label_33)


        self.verticalLayout_2.addWidget(self.frame)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.retranslateUi(Information)

        QMetaObject.connectSlotsByName(Information)
    # setupUi

    def retranslateUi(self, Information):
        Information.setWindowTitle(QCoreApplication.translate("Information", u"Information", None))
        self.label_10.setText(QCoreApplication.translate("Information", u"Introduction", None))
        self.label_3.setText(QCoreApplication.translate("Information", u"This  page contains information on the general rules for a sudoku as well as information \n"
" on how to solve them. In the first part the rules are explained and in the second part some algorithms \n"
"are given that will help you solve sudokus. When using one of the hint buttons the computer finds a hint \n"
"using one of these algorithms.", None))
        self.label_11.setText(QCoreApplication.translate("Information", u"Part 1: Rulesets for different sudoku types", None))
        self.label_4.setText(QCoreApplication.translate("Information", u"Here is an example of a standard 9x9 grid:", None))
        self.label_7.setText("")
        self.label.setText(QCoreApplication.translate("Information", u"1.1 Grid Structure:\n"
"   - The puzzle is divided into a grid of cells.\n"
"   - The grid is further subdivided into smaller regions.\n"
"   - In a standard 9x9 Sudoku, these regions are 3x3 squares.\n"
"     for 4x4, these regions are 2x2 squares and for 16x16 these are\n"
"     4x4 squares", None))
        self.label_2.setText(QCoreApplication.translate("Information", u"1.2 Rules:\n"
"   - Fill in the grid with numbers from 1 to the size of the grid.\n"
"   - Each row, column, and region must contain all numbers from 1\n"
"      to the size of the grid with no repetitions.\n"
"   - Once the grid is completely filled the puzzle is completed", None))
        self.label_5.setText(QCoreApplication.translate("Information", u"Part 2: Algorithms for solving sudokus", None))
        self.label_6.setText(QCoreApplication.translate("Information", u"2.1 Hidden Singles:", None))
        self.label_8.setText(QCoreApplication.translate("Information", u"Finding Hidden Singles in a Sudoku puzzle involves identifying a cell within a specific row, column, or \n"
"box that is the only possible position for a certain number, even though it may not be immediately \n"
"apparent due to the presence of other candidate numbers in that cell.", None))
        self.label_9.setText(QCoreApplication.translate("Information", u"This situation arises when, upon closer examination, the chosen number is eliminated as a possibility \n"
"in all other cells within the unit (row, column, or box) due to the constraints imposed by numbers \n"
"already placed in intersecting rows, columns, or boxes. The Hidden Single is thus \"hidden\" among \n"
"other candidates but is, in fact, the sole valid number for that cell.", None))
        self.label_12.setText(QCoreApplication.translate("Information", u"Below is an example of a 4 that is the last possible candidate:", None))
        self.label_13.setText("")
        self.label_14.setText(QCoreApplication.translate("Information", u"2.2 Hidden Pairs:", None))
        self.label_15.setText(QCoreApplication.translate("Information", u"Hidden pairs, triples, and quads are techniques used in Sudoku solving that help to eliminate \n"
"candidates from cells, making the puzzle easier to solve. Unlike naked pairs, triples, and quads, \n"
"where the focus is on the candidates that are visible across multiple cells, hidden techniques \n"
"spotlight the candidates that are subtly exclusive to a set of cells within a unit (row, column, or box) \n"
"but are obscured by the presence of additional candidates.\n"
"\n"
" Let's look at the different variations", None))
        self.label_24.setText(QCoreApplication.translate("Information", u"Hidden Pairs", None))
        self.label_25.setText(QCoreApplication.translate("Information", u"A hidden pair occurs when two numbers appear as candidates only in the same two cells within a \n"
"unit, even though those cells might contain additional candidates. Since those two numbers must \n"
"occupy those two cells (because they don't appear as candidates in any other cells in that unit), all \n"
"other candidates can be eliminated from these two cells.", None))
        self.label_26.setText(QCoreApplication.translate("Information", u"Hidden Triples", None))
        self.label_27.setText(QCoreApplication.translate("Information", u"A hidden triple exists when three numbers are confined to three cells within a unit, even if those cells \n"
"also list other candidates. The key is that these three numbers don't appear as candidates in any cells \n"
"outside this trio within the unit. Identifying a hidden triple allows you to remove all other candidates \n"
"from these three cells.", None))
        self.label_28.setText(QCoreApplication.translate("Information", u"Hidden Quads", None))
        self.label_29.setText(QCoreApplication.translate("Information", u"A hidden quad occurs when four numbers are limited to exactly four cells within a unit, despite those \n"
"cells possibly containing additional numbers as candidates. This pattern means these four numbers \n"
"cannot be candidates in any other cells within the unit. You can remove all other candidates from \n"
"these four cells.", None))
        self.label_16.setText(QCoreApplication.translate("Information", u"\n"
"2.3 Naked Pairs:", None))
        self.label_17.setText(QCoreApplication.translate("Information", u"Naked pairs, triples, and quads are advanced Sudoku solving techniques that can help you eliminate \n"
"candidates from cells and move closer to solving the puzzle. These strategies are based on the \n"
"principle that if a certain number of cells in a row, column, or box (unit) can only contain a unique set \n"
"of numbers, then those numbers can be eliminated as candidates from all other cells in that unit.\n"
"\n"
"Just like Hidden pairs we have 3 variations.", None))
        self.label_18.setText(QCoreApplication.translate("Information", u"\n"
"Naked Pairs", None))
        self.label_19.setText(QCoreApplication.translate("Information", u"A naked pair occurs when two cells within the same unit (row, column, or box) have the same two \n"
"candidates and only those two. This means both numbers must be confined to those two cells within \n"
"that unit. Since those two numbers must occupy those two cells, they can be eliminated as \n"
"candidates from all other cells in the unit.", None))
        self.label_20.setText(QCoreApplication.translate("Information", u"Naked Triples", None))
        self.label_21.setText(QCoreApplication.translate("Information", u"A naked triple occurs when three cells within a unit contain the same three candidates or any subset \n"
"of those three candidates, and no other candidates are in those cells. The key is that between these \n"
"three cells, only three numbers are possible. This means those three numbers can only be in these \n"
"three cells and can be eliminated as candidates from all other cells in the unit.", None))
        self.label_22.setText(QCoreApplication.translate("Information", u"Naked Quads", None))
        self.label_23.setText(QCoreApplication.translate("Information", u"A naked quad occurs when four cells within a unit contain the same four candidates or any subset \n"
"thereof, with no other candidates in those cells. This situation means those four numbers are locked \n"
"into those four cells within the unit, allowing you to eliminate those numbers from the candidates of \n"
"all other cells in the unit.", None))
        self.label_30.setText(QCoreApplication.translate("Information", u"\n"
"2.4 Pointing Pairs", None))
        self.label_31.setText(QCoreApplication.translate("Information", u"Pointing pairs (or pointing tuples) is a technique in Sudoku solving that helps in eliminating \n"
"candidates from cells. It occurs when all possible locations for a certain number within a box (one of \n"
"the nine 3x3 sections) line up in a single row or column. Because the number must appear in that row \n"
"or column within the box, it cannot appear in the same row or column outside of that box. This \n"
"allows you to eliminate that number as a candidate from other cells in the row or column outside the \n"
"box.\n"
"\n"
"**How Pointing Pairs Work:**\n"
"\n"
"\n"
"1.Identification: Start by identifying a scenario where a specific number can only fit in two or \n"
"three cells within a box, and these cells align either horizontally or vertically (all in the same \n"
"row or column).\n"
"\n"
"2.Implication: The alignment implies that this number must occupy one of these cells within \n"
"the box, and as such, it cannot appear in the remainder of the row or column outside of this \n"
"box.\n"
"\n"
"3.Elimin"
                        "ation: You can then safely eliminate this number as a candidate from other cells in the \n"
"same row or column outside the box, simplifying the puzzle.\n"
"", None))
        self.label_32.setText(QCoreApplication.translate("Information", u"2.5 Box Line Reduction", None))
        self.label_33.setText(QCoreApplication.translate("Information", u"Box Line Reduction, similar to Pointing Pairs, is a technique used in Sudoku solving that helps to \n"
"eliminate candidates from cells. This technique is based on the interaction between a box (one of the \n"
"nine 3x3 sections) and a row or column. Box Line Reduction occurs when all possible placements of a \n"
"number within a row or column fall within a single box. Since that number must then appear in that \n"
"row or column within that box, it cannot be a candidate for any other cells in the box outside of that \n"
"specific row or column.\n"
"\n"
"\n"
"**How Box Line Reduction Works**\n"
"\n"
"1. Identification: First, identify a row or column where a certain number can only appear within the \n"
"cells that fall inside a single box. The key observation is that this number does not have any possible \n"
"placements in the row or column outside this box.\n"
"\n"
"2. Implication: Because the number must occupy one of these cells within the intersecting row or \n"
"column inside the box, it is logically ex"
                        "cluded from being in any other cell in the box that does not \n"
"align with the identified row or column.\n"
"\n"
"3. Elimination: As a result, you can eliminate this number as a candidate from the rest of the cells in \n"
"the box that are outside of the intersecting row or column.\n"
"", None))
    # retranslateUi

