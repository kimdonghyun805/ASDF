
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
        self.kind = "test_widget1"
        self.resize(self.size_x, self.size_y)
        self.is_connecting = False
        self.is_connected = False
        
        self.textfield = QTextEdit(self)
        self.textfield.resize(self.size_x - 10, self.size_y - 10)
        self.textfield.move(5, 5)
        print("test_widget1 created")

    def connectWidget(self) :
        print("do connectWidget 1")

    def editData(self, name) :
        self.name = str(name)

    def getData(self) :
        print("do getWidgetData 1")
        data = {}
        data["name"] = self.name
        data["order"] = self.order
        data["kind"] = self.kind
        data["size_x"] = self.size_x
        data["size_y"] = self.size_y
        data["is_connected"] = self.is_connected
        data["is_connecting"] = self.is_connecting
        return data

    def setData(self, data) :
        self.name = data["name"]
        self.order = data["order"]
        #self.kind = data["kind"] # 재설정할 필요 없는 데이터
        self.size_x = data["size_x"]
        self.size_y = data["size_y"]
        self.is_connected = data["is_connected"]
        #self.is_connecting = data["is_connecting"] # 재설정할 필요 없는 데이터
        # 입력되는 데이터에 따라 위젯을 조정함
        self.resize(self.size_x, self.size_y)
        self.textfield.resize(self.size_x - 10, self.size_y - 10)

    def setOrder(self, order) : self.order = int(order)

    def getOrder(self) : return self.order

    def getInfo(self) :
        info = "widget information of test_widget1"
        info = info + " 테스트 위젯 1에 대한 정보"
        return info

    def getName(self) : return self.name

    def setName(self, name) : self.name = str(name)

    def getKind(self) : return self.kind

    def getSize(self) : return (self.size_x, self.size_y)

    def deleteWidget(self) :
        print("do deleteWidget")