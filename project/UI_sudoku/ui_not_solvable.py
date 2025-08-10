# -*- coding: utf-8 -*-
# pylint: skip-file

################################################################################
## Form generated from reading UI file 'not_solvableckxkaO.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QSizePolicy,
    QWidget)

class Ui_IncorrectSolution(object):
    def setupUi(self, IncorrectSolution):
        if not IncorrectSolution.objectName():
            IncorrectSolution.setObjectName(u"IncorrectSolution")
        IncorrectSolution.resize(470, 223)
        IncorrectSolution.setContextMenuPolicy(Qt.CustomContextMenu)
        IncorrectSolution.setStyleSheet(u"background-color: rgb(229, 0, 0);")
        self.label = QLabel(IncorrectSolution)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 50, 470, 51))
        font = QFont()
        font.setPointSize(17)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label_2 = QLabel(IncorrectSolution)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(0, 105, 470, 31))
        font1 = QFont()
        font1.setPointSize(12)
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignCenter)
        self.pushButton = QPushButton(IncorrectSolution)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(140, 160, 181, 41))
        self.pushButton.setStyleSheet(u"background-color: rgb(85, 170, 0);")

        self.retranslateUi(IncorrectSolution)

        QMetaObject.connectSlotsByName(IncorrectSolution)
    # setupUi

    def retranslateUi(self, IncorrectSolution):
        IncorrectSolution.setWindowTitle(QCoreApplication.translate("IncorrectSolution", u"Form", None))
        self.label.setText(QCoreApplication.translate("IncorrectSolution", u"!! The uploaded Sudoku is not solvable !!", None))
        self.label_2.setText(QCoreApplication.translate("IncorrectSolution", u"Please check that the uploaded Sudoku is correct", None))
        self.pushButton.setText(QCoreApplication.translate("IncorrectSolution", u"return to upload window", None))
    # retranslateUi

