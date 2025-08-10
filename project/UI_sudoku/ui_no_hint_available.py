# -*- coding: utf-8 -*-
# pylint: skip-file

################################################################################
## Form generated from reading UI file 'no_hint_availableBEFMDR.ui'
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

class Ui_no_hint_available(object):
    def setupUi(self, no_hint_available):
        if not no_hint_available.objectName():
            no_hint_available.setObjectName(u"no_hint_available")
        no_hint_available.resize(545, 302)
        no_hint_available.setStyleSheet(u"background-color: rgb(163, 223, 249);")
        self.label = QLabel(no_hint_available)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 20, 545, 131))
        font = QFont()
        font.setPointSize(25)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label_2 = QLabel(no_hint_available)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(0, 160, 545, 101))
        font1 = QFont()
        font1.setPointSize(13)
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignCenter)
        self.pushButton = QPushButton(no_hint_available)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(200, 260, 141, 24))
        font2 = QFont()
        font2.setPointSize(11)
        font2.setBold(True)
        self.pushButton.setFont(font2)
        self.pushButton.setStyleSheet(u"background-color: rgb(0, 170, 0);")

        self.retranslateUi(no_hint_available)

        QMetaObject.connectSlotsByName(no_hint_available)
    # setupUi

    def retranslateUi(self, no_hint_available):
        no_hint_available.setWindowTitle(QCoreApplication.translate("no_hint_available", u"No Hint Available!", None))
        self.label.setText(QCoreApplication.translate("no_hint_available", u"This hint is not available\n"
"right now", None))
        self.label_2.setText(QCoreApplication.translate("no_hint_available", u"With the current sudoku grid, this hint is not possible.\n"
"\n"
"Give one of our other hints a try if you're stuck!", None))
        self.pushButton.setText(QCoreApplication.translate("no_hint_available", u"Got it!", None))
    # retranslateUi

