# -*- coding: utf-8 -*-
# pylint: skip-file

################################################################################
## Form generated from reading UI file 'main_windowvejdHe.ui'
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

class Ui_Mainwindow(object):
    def setupUi(self, Mainwindow):
        if not Mainwindow.objectName():
            Mainwindow.setObjectName(u"Mainwindow")
        Mainwindow.resize(900, 700)
        Mainwindow.setTabletTracking(False)
        Mainwindow.setStyleSheet(u"background-color: rgb(85, 255, 255);\n"
"background-color: rgb(163, 223, 249);")
        self.label = QLabel(Mainwindow)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(190, 30, 501, 251))
        font = QFont()
        font.setFamilies([u"Snap ITC"])
        font.setPointSize(36)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.button1 = QPushButton(Mainwindow)
        self.button1.setObjectName(u"button1")
        self.button1.setGeometry(QRect(140, 310, 241, 121))
        font1 = QFont()
        font1.setPointSize(16)
        font1.setBold(False)
        self.button1.setFont(font1)
        self.button1.setStyleSheet(u"background-color: rgb(255, 0, 0);")
        self.button2 = QPushButton(Mainwindow)
        self.button2.setObjectName(u"button2")
        self.button2.setGeometry(QRect(490, 310, 241, 121))
        self.button2.setFont(font1)
        self.button2.setStyleSheet(u"background-color: rgb(0, 170, 0);")

        self.retranslateUi(Mainwindow)

        QMetaObject.connectSlotsByName(Mainwindow)
    # setupUi

    def retranslateUi(self, Mainwindow):
        Mainwindow.setWindowTitle(QCoreApplication.translate("Mainwindow", u"Main Menu", None))
        self.label.setText(QCoreApplication.translate("Mainwindow", u"SUDOKU MASTER", None))
        self.button1.setText(QCoreApplication.translate("Mainwindow", u"Upload new Sudoku", None))
        self.button2.setText(QCoreApplication.translate("Mainwindow", u"Generate new Sudoku", None))
    # retranslateUi

