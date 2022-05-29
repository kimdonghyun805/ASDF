

from PyQt5.QtWidgets import (QWidget, QScrollArea, QPushButton, QDialog,
                             QLabel, QTextEdit, QLineEdit, QGroupBox)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QSize, QPoint, Qt, pyqtSignal

class test_widget2 (QWidget) :

    def __init__(self, name, order, x : int, y=77, z=99) :
        super().__init__()

        self.name = str(name)
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
        self.order = int(order)
        self.kind = "test_widget2"
        self.is_connecting = False
        self.is_connected = True

        self.size_x = 200
        self.size_y = 200
        self.resize(self.size_x, self.size_y)

        self.widget = QGroupBox(self)
        self.widget.resize(self.size_x - 5, self.size_y - 5)
        #self.widget.setParent(self)
        #self.widget.show()

        self.label_name = QLabel(self.name, self.widget)
        self.label_name.move(20, 20)
        self.label_x = QLabel(str(self.x), self.widget)
        self.label_x.move(20, 50)
        self.label_y = QLabel(str(self.y), self.widget)
        self.label_y.move(20, 80)
        self.label_z = QLabel(str(self.z), self.widget)
        self.label_z.move(20, 110)

    def connectWidget(self) :
        print("do connectWidget 2")

    def editData(self, name, x, y) : 
        # 위젯의 특정 데이터를 수정
        self.name = str(name)
        self.size_x = int(x)
        self.size_y = int(y)
        # 입력되는 데이터에 따라 위젯을 조정
        self.resize(self.size_x, self.size_y)
        self.widget.resize(self.size_x - 5, self.size_y - 5)

    def getData(self) :
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
        # 입력되는 데이터에 따라 위젯을 조정
        self.resize(self.size_x, self.size_y)
        self.widget.resize(self.size_x - 5, self.size_y - 5)

    def getOrder(self) : return self.order

    def setOrder(self, order) : self.order = int(order)

    def getInfo(self) : return "info about test_widget2"

    def getSize(self) : return (self.size_x, self.size_y)

    def getName(self) : return self.name

    def setName(self, name) : self.name = str(name)

    def getKind(self) : return self.kind

    def deleteWidget(self) : pass

