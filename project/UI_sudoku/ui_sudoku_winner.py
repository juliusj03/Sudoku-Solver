# -*- coding: utf-8 -*-
# pylint: skip-file

################################################################################
## Form generated from reading UI file 'sudoku_winnerPBNffr.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QSizePolicy, QWidget)

class Ui_WinnerWindow(object):
    def setupUi(self, WinnerWindow):
        if not WinnerWindow.objectName():
            WinnerWindow.setObjectName(u"WinnerWindow")
        WinnerWindow.resize(545, 360)
        WinnerWindow.setStyleSheet(u"background-color: rgb(163, 223, 249);")
        self.label = QLabel(WinnerWindow)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 40, 545, 131))
        font = QFont()
        font.setPointSize(38)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label_2 = QLabel(WinnerWindow)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(0, 180, 545, 61))
        font1 = QFont()
        font1.setPointSize(13)
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.retranslateUi(WinnerWindow)

        QMetaObject.connectSlotsByName(WinnerWindow)
    # setupUi

    def retranslateUi(self, WinnerWindow):
        WinnerWindow.setWindowTitle(QCoreApplication.translate("WinnerWindow", u"Form", None))
        self.label.setText(QCoreApplication.translate("WinnerWindow", u"Congratulations!", None))
        self.label_2.setText(QCoreApplication.translate("WinnerWindow", u"You have completed the Sudoku! And we are so proud of you :)", None))
    # retranslateUi

