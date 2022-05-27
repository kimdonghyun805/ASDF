
from PyQt5.QtWidgets import (QWidget, QScrollArea, QPushButton, QDialog,
                             QLabel, QTextEdit, QLineEdit, QGroupBox)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QSize, QPoint, Qt, pyqtSignal

class test_widget1 (QWidget) :
    def __init__(self, name) :
        super().__init__()

        self.size_x = 400
        self.size_y = 400
        self.name = str(name)
        self.order = 0
        self.resize(self.size_x, self.size_y)
        
        self.textfield = QTextEdit(self)
        self.textfield.resize(self.size_x - 10, self.size_y - 10)
        self.textfield.move(5, 5)
        print("test_widget1 created")

    def connectWidget(self) :
        print("do connectWidget 1")

    def getData(self) :
        print("do getWidgetData 1")
        info = []
        info.append(self.size_x)
        info.append(self.size_y)
        return info

    def setData(self, name, x, y) :
        self.name = str(name)
        self.size_x = int(x)
        self.size_y = int(y)
        self.resize(self.size_x, self.size_y)
        self.textfield.resize(self.size_x - 10, self.size_y - 10)

    def setOrder(self, order) :
        self.order = order
        print("do setOrder")

    def getOrder(self) : 
        print("do getOrder")
        return self.order

    def getInfo(self) :
        info = "widget information of test_widget1"
        info = info + " 테스트 위젯 1에 대한 정보"
        return info

    def getName(self) : return self.name

    def setName(self, name) : self.name = str(name)

    def getKind(self) : return self.kind

    def getSize(self) :
        print("do getSize")
        return (self.size_x, self.size_y)

    def deleteWidget(self) :
        print("do deleteWidget")