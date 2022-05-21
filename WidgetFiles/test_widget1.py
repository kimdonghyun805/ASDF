
from PyQt5.QtWidgets import (QWidget, QScrollArea, QPushButton, QDialog,
                             QLabel, QTextEdit, QLineEdit, QGroupBox)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QSize, QPoint, Qt, pyqtSignal

class test_widget1 (QWidget) :
    x = 2
    y = 3
    def __init__(self) :
        super().__init__()

        self.size_x = 400
        self.size_y = 400
        self.order = -1
        self.resize(self.size_x, self.size_y)
        z = 4
        self.textfield = QTextEdit()
        self.textfield.resize(self.size_x, self.size_y)

    def connectWidget(self) :
        print("do connectWidget 1")

    def getData(self) :
        print("do getWidgetData 1")
        info = []
        info.append(self.size_x)
        info.append(self.size_y)
        return info

    def setData(self, x, y) :
        self.size_x = x
        self.size_y = y
        self.resize(self.size_x, self.size_y)
        self.textfield.resize(self.size_x, self.size_y)
        print("do setWidgetData 1", str(self.size_x), str(self.size_y))

    def setOrder(self, order) :
        self.order = order
        print("do setOrder")

    def getOrder(self) : 
        print("do getOrder")
        return self.order

    def getInfo(self) :
        info = "widget information of test_widget1"
        info = info + "테스트 위젯 1에 대한 정보"
        return info

    def setLocation(self, x, y) :
        print("do setLocation")

    def deleteWidget(self) :
        print("do deleteWidget")