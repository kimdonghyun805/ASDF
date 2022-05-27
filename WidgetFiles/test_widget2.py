

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

        self.size_x = 400
        self.size_y = 400
        self.resize(self.size_x, self.size_y)

        self.widget = QGroupBox(self)
        self.widget.resize(self.size_x, self.size_y)
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

    def getData(self) :
        print("do getWidgetData 2")

    def setData(self, name, x, y) :
        self.name = str(name)
        self.size_x = int(x)
        self.size_y = int(y)
        self.resize(self.size_x, self.size_y)
        self.textfield.resize(self.size_x, self.size_y)
        print("do setWidgetData 2", str(self.size_x), str(self.size_y))

    def getOrder(self) : return self.order

    def setOrder(self, order) : self.order = order

    def getInfo(self) : pass

    def getSize(self) : return (self.size_x, self.size_y)

    def getName(self) : return self.name

    def setName(self, name) : self.name = str(name)

    def getKind(self) : return self.kind

    def deleteWidget(self) : pass

