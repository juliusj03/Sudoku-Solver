# -*- coding: utf-8 -*-
# pylint: skip-file

################################################################################
## Form generated from reading UI file 'size_selection_screen.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QPushButton,
    QSizePolicy, QWidget)

class Ui_SelectionScreen(object):
    def setupUi(self, SelectionScreen):
        if not SelectionScreen.objectName():
            SelectionScreen.setObjectName(u"SelectionScreen")
        SelectionScreen.resize(900, 700)
        SelectionScreen.setStyleSheet(u"background-color: rgb(85, 255, 255);\n"
"background-color: rgb(163, 223, 249);")
        self.Pb_4x4 = QPushButton(SelectionScreen)
        self.Pb_4x4.setObjectName(u"Pb_4x4")
        self.Pb_4x4.setGeometry(QRect(44, 310, 241, 121))
        font = QFont()
        font.setPointSize(16)
        self.Pb_4x4.setFont(font)
        self.Pb_4x4.setStyleSheet(u"background-color: rgb(255, 0, 0);")
        self.Pb_9x9 = QPushButton(SelectionScreen)
        self.Pb_9x9.setObjectName(u"Pb_9x9")
        self.Pb_9x9.setGeometry(QRect(329, 310, 241, 121))
        self.Pb_9x9.setFont(font)
        self.Pb_9x9.setStyleSheet(u"background-color: rgb(255, 0, 0);")
        self.Pb_16x16 = QPushButton(SelectionScreen)
        self.Pb_16x16.setObjectName(u"Pb_16x16")
        self.Pb_16x16.setGeometry(QRect(614, 310, 241, 121))
        self.Pb_16x16.setFont(font)
        self.Pb_16x16.setStyleSheet(u"background-color: rgb(255, 0, 0);")
        self.lb_instuctions = QLabel(SelectionScreen)
        self.lb_instuctions.setObjectName(u"lb_instuctions")
        self.lb_instuctions.setGeometry(QRect(150, 100, 600, 40))
        font1 = QFont()
        font1.setPointSize(20)
        self.lb_instuctions.setFont(font1)
        self.lb_instuctions.setAlignment(Qt.AlignCenter)
        self.return_main = QPushButton(SelectionScreen)
        self.return_main.setObjectName(u"return_main")
        self.return_main.setGeometry(QRect(20, 20, 121, 61))
        self.return_main.setStyleSheet(u"background-color: rgb(255, 170, 0);\n"
"font: 9pt \"Tempus Sans ITC\";")
        self.comboBox = QComboBox(SelectionScreen)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(329, 210, 241, 22))
        self.comboBox.setStyleSheet(u"\n"
"background-color: rgb(255, 255, 255);")

        self.retranslateUi(SelectionScreen)

        QMetaObject.connectSlotsByName(SelectionScreen)
    # setupUi

    def retranslateUi(self, SelectionScreen):
        SelectionScreen.setWindowTitle(QCoreApplication.translate("SelectionScreen", u"Size selection screen", None))
        self.Pb_4x4.setText(QCoreApplication.translate("SelectionScreen", u"4x4", None))
        self.Pb_9x9.setText(QCoreApplication.translate("SelectionScreen", u"9x9", None))
        self.Pb_16x16.setText(QCoreApplication.translate("SelectionScreen", u"16x16", None))
        self.lb_instuctions.setText(QCoreApplication.translate("SelectionScreen", u"Please select a mode and size for the sudoku", None))
        self.return_main.setText(QCoreApplication.translate("SelectionScreen", u"Return to\n"
"main menu", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("SelectionScreen", u"Standard", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("SelectionScreen", u"Diagonal", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("SelectionScreen", u"Chess", None))

    # retranslateUi

