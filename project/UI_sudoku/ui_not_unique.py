# -*- coding: utf-8 -*-
# pylint: skip-file

################################################################################
## Form generated from reading UI file 'not_unique.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QSizePolicy,
    QWidget)

class Ui_SeveralSolution(object):
    def setupUi(self, SeveralSolution):
        if not SeveralSolution.objectName():
            SeveralSolution.setObjectName(u"SeveralSolution")
        SeveralSolution.resize(550, 223)
        SeveralSolution.setContextMenuPolicy(Qt.CustomContextMenu)
        SeveralSolution.setStyleSheet(u"background-color: rgb(229, 0, 0);")
        self.label = QLabel(SeveralSolution)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(25, 50, 500, 51))
        font = QFont()
        font.setPointSize(17)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label_2 = QLabel(SeveralSolution)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(25, 105, 470, 41))
        font1 = QFont()
        font1.setPointSize(12)
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignCenter)
        self.return_button = QPushButton(SeveralSolution)
        self.return_button.setObjectName(u"return_button")
        self.return_button.setGeometry(QRect(70, 160, 181, 41))
        self.return_button.setStyleSheet(u"background-color: rgb(85, 170, 0);")
        self.continue_button = QPushButton(SeveralSolution)
        self.continue_button.setObjectName(u"continue_button")
        self.continue_button.setGeometry(QRect(290, 160, 181, 41))
        self.continue_button.setStyleSheet(u"background-color: rgb(170, 0, 0);")

        self.retranslateUi(SeveralSolution)

        QMetaObject.connectSlotsByName(SeveralSolution)
    # setupUi

    def retranslateUi(self, SeveralSolution):
        SeveralSolution.setWindowTitle(QCoreApplication.translate("SeveralSolution", u"warning", None))
        self.label.setText(QCoreApplication.translate("SeveralSolution", u"!! The uploaded Sudoku has several solutions!!", None))
        self.label_2.setText(QCoreApplication.translate("SeveralSolution", u"Your solution might differ from the solution used by the program.\n"
"Do you wish to continue?", None))
        self.return_button.setText(QCoreApplication.translate("SeveralSolution", u"return to upload window", None))
        self.continue_button.setText(QCoreApplication.translate("SeveralSolution", u"continue to playing window", None))
    # retranslateUi

