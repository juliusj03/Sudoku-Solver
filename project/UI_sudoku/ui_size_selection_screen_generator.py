# -*- coding: utf-8 -*-
# pylint: skip-file

################################################################################
## Form generated from reading UI file 'size_selection_screen_generatorpxSktA.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QPushButton,
    QSizePolicy, QWidget)

class Ui_SelectionScreenGenerator(object):
    def setupUi(self, SelectionScreenGenerator):
        if not SelectionScreenGenerator.objectName():
            SelectionScreenGenerator.setObjectName(u"SelectionScreenGenerator")
        SelectionScreenGenerator.resize(900, 700)
        SelectionScreenGenerator.setStyleSheet(u"background-color: rgb(85, 255, 255);\n"
"background-color: rgb(163, 223, 249);")
        self.Pb_4x4 = QPushButton(SelectionScreenGenerator)
        self.Pb_4x4.setObjectName(u"Pb_4x4")
        self.Pb_4x4.setGeometry(QRect(180, 310, 241, 121))
        font = QFont()
        font.setPointSize(16)
        self.Pb_4x4.setFont(font)
        self.Pb_4x4.setStyleSheet(u"background-color: rgb(255, 0, 0);")
        self.Pb_9x9 = QPushButton(SelectionScreenGenerator)
        self.Pb_9x9.setObjectName(u"Pb_9x9")
        self.Pb_9x9.setGeometry(QRect(480, 310, 241, 121))
        self.Pb_9x9.setFont(font)
        self.Pb_9x9.setStyleSheet(u"background-color: rgb(255, 0, 0);")
        self.lb_instuctions = QLabel(SelectionScreenGenerator)
        self.lb_instuctions.setObjectName(u"lb_instuctions")
        self.lb_instuctions.setGeometry(QRect(50, 160, 800, 40))
        font1 = QFont()
        font1.setPointSize(20)
        self.lb_instuctions.setFont(font1)
        self.lb_instuctions.setAlignment(Qt.AlignCenter)
        self.return_main = QPushButton(SelectionScreenGenerator)
        self.return_main.setObjectName(u"return_main")
        self.return_main.setGeometry(QRect(20, 20, 121, 61))
        self.return_main.setStyleSheet(u"background-color: rgb(255, 170, 0);\n"
"font: 9pt \"Tempus Sans ITC\";")
        self.lb_generating = QLabel(SelectionScreenGenerator)
        self.lb_generating.setObjectName(u"lb_generating")
        self.lb_generating.setGeometry(QRect(140, 200, 600, 30))
        font2 = QFont()
        font2.setPointSize(15)
        self.lb_generating.setFont(font2)
        self.lb_generating.setStyleSheet(u"")
        self.lb_generating.setAlignment(Qt.AlignCenter)
        self.comboBox = QComboBox(SelectionScreenGenerator)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(415, 250, 70, 22))
        self.comboBox.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.wait_label = QLabel(SelectionScreenGenerator)
        self.wait_label.setObjectName(u"wait_label")
        self.wait_label.setGeometry(QRect(0, 500, 921, 131))
        self.wait_label.setFont(font2)
        self.wait_label.setAlignment(Qt.AlignCenter)

        self.retranslateUi(SelectionScreenGenerator)

        QMetaObject.connectSlotsByName(SelectionScreenGenerator)
    # setupUi

    def retranslateUi(self, SelectionScreenGenerator):
        SelectionScreenGenerator.setWindowTitle(QCoreApplication.translate("SelectionScreenGenerator", u"Size selection screen", None))
        self.Pb_4x4.setText(QCoreApplication.translate("SelectionScreenGenerator", u"4x4", None))
        self.Pb_9x9.setText(QCoreApplication.translate("SelectionScreenGenerator", u"9x9", None))
        self.lb_instuctions.setText(QCoreApplication.translate("SelectionScreenGenerator", u"Please select a difficulty and size for the sudoku to be generated", None))
        self.return_main.setText(QCoreApplication.translate("SelectionScreenGenerator", u"Return to\n"
"main menu", None))
        self.lb_generating.setText(QCoreApplication.translate("SelectionScreenGenerator", u"(generating can take up to a minute)", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("SelectionScreenGenerator", u"easy", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("SelectionScreenGenerator", u"normal", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("SelectionScreenGenerator", u"hard", None))

        self.wait_label.setText(QCoreApplication.translate("SelectionScreenGenerator", u"We are generating a sudoku just for you!\n"
"Please give us some time to complete the process.", None))
    # retranslateUi

