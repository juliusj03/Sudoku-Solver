# -*- coding: utf-8 -*-
# pylint: skip-file

################################################################################
## Form generated from reading UI file 'confirm_return_to_mainiFTPGu.ui'
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

class Ui_ConfirmToMain(object):
    def setupUi(self, ConfirmToMain):
        if not ConfirmToMain.objectName():
            ConfirmToMain.setObjectName(u"ConfirmToMain")
        ConfirmToMain.resize(410, 200)
        ConfirmToMain.setStyleSheet(u"background-color: rgb(255, 170, 0);\n"
"")
        self.label = QLabel(ConfirmToMain)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, -20, 410, 200))
        font = QFont()
        font.setFamilies([u"Verdana"])
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.ok_button = QPushButton(ConfirmToMain)
        self.ok_button.setObjectName(u"ok_button")
        self.ok_button.setGeometry(QRect(70, 150, 91, 24))
        self.ok_button.setStyleSheet(u"background-color: rgb(170, 85, 255);")
        self.cancel_button = QPushButton(ConfirmToMain)
        self.cancel_button.setObjectName(u"cancel_button")
        self.cancel_button.setGeometry(QRect(244, 150, 91, 24))
        self.cancel_button.setStyleSheet(u"background-color: rgb(0, 170, 127);")

        self.retranslateUi(ConfirmToMain)

        QMetaObject.connectSlotsByName(ConfirmToMain)
    # setupUi

    def retranslateUi(self, ConfirmToMain):
        ConfirmToMain.setWindowTitle(QCoreApplication.translate("ConfirmToMain", u"Return To main", None))
        self.label.setText(QCoreApplication.translate("ConfirmToMain", u"Are you sure?\n"
"\n"
" If you go back to the main menu\n"
" you're current sudoku will be lost", None))
        self.ok_button.setText(QCoreApplication.translate("ConfirmToMain", u"OK", None))
        self.cancel_button.setText(QCoreApplication.translate("ConfirmToMain", u"Cancel", None))
    # retranslateUi

