

from PyQt5.QtWidgets import (QWidget, QScrollArea, QPushButton, QDialog,
                             QLabel, QTextEdit, QLineEdit, QGroupBox)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QSize, QPoint, Qt, pyqtSignal

class test_widget2 (QWidget) :

    def __init__(self) :
        super().__init__()

        self.size_x = 400
        self.size_y = 400
        self.resize(self.size_x, self.size_y)

        self.textfield = QTextEdit()
        self.textfield.resize(self.size_x, self.size_y)

    def connectWidget(self) :
        print("do connectWidget 2")

    def getWidgetData(self) :
        print("do getWidgetData 2")

    def setWidgetData(self, x, y) :
        self.size_x = x
        self.size_y = y
        self.resize(self.size_x, self.size_y)
        self.textfield.resize(self.size_x, self.size_y)
        print("do setWidgetData 2", str(self.size_x), str(self.size_y))
