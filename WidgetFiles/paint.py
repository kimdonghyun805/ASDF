import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class paint (QWidget) :
    def __init__(self, name) : # 생성시 필요한 데이터를 생성자의 파라미터로 지정
        super().__init__()

        self.name = str(name) # 이 위젯 고유의 이름, 생성시 설정
        
        self.order = 0 # 위젯의 식별 번호, 각 위젯이 고유 값을 가짐, 생성시 설정, 변경 불가능

        # 위젯의 종류에 따라 사용자 임의로 설정, 실행 중 변경 불가능
        self.kind = "paint" # 위젯의 종류, 위젯 파일의 이름
        self.size_x = 400 # 위젯의 가로 길이, 폭
        self.size_y = 400 # 위젯의 세로 길이, 높이

        # 위젯의 종류에 따라 사용자 임의로 설정, 실행 중 변경 가능
        self.is_connected = False # 위젯이 연결되었는지 확인
        self.is_connecting = False # 위젯이 연결 대상이 필요한지 확인
        self.list_widget_connected = [] # 연결하여 사용중인 위젯의 목록, 연결 위젯인 경우만 필요

        self.resize(self.size_x, self.size_y) # 크기 설정

        ######################## 위젯 내용 작성 #######################
        self.font = QFont("Arial", 10)
        self.font.setPixelSize(12)
        self.setStyleSheet("background-color : #FFFFFFFF")

        self.image = QImage(QSize(self.size_x, self.size_y), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.drawing = False
        self.brush_size = 2
        self.brush_color = Qt.black
        self.last_point = QPoint()

        self.thick_btn = QPushButton("굵게",self)
        self.thick_btn.clicked.connect(self.size_up)
        self.thick_btn.setFont(self.font)
        self.thick_btn.resize(40, 30)
        self.thick_btn.move(0, 0)

        self.thin_btn = QPushButton("얇게",self)
        self.thin_btn.clicked.connect(self.size_down)
        self.thin_btn.setFont(self.font)
        self.thin_btn.resize(40, 30)
        self.thin_btn.move(40, 0)

        self.black_btn = QPushButton("검정",self)
        self.black_btn.clicked.connect(self.set_color_black)
        self.black_btn.setFont(self.font)
        self.black_btn.resize(40, 30)
        self.black_btn.move(80, 0)

        self.red_btn = QPushButton("빨강",self)
        self.red_btn.clicked.connect(self.set_color_red)
        self.red_btn.setFont(self.font)
        self.red_btn.resize(40, 30)
        self.red_btn.move(120, 0)

        self.blue_btn = QPushButton("파랑",self)
        self.blue_btn.clicked.connect(self.set_color_blue)
        self.blue_btn.setFont(self.font)
        self.blue_btn.resize(40, 30)
        self.blue_btn.move(160, 0)

        self.green_btn = QPushButton("초록",self)
        self.green_btn.clicked.connect(self.set_color_green)
        self.green_btn.setFont(self.font)
        self.green_btn.resize(40, 30)
        self.green_btn.move(200, 0)

        self.green_btn = QPushButton("모두 지우기",self)
        self.green_btn.clicked.connect(self.clear_image)
        self.green_btn.setFont(self.font)
        self.green_btn.resize(80, 30)
        self.green_btn.move(280, 0)

        ##################### 위젯 내용 작성 종료 #######################


    ######################### 필수 함수 #############################
    # 필수 함수 editData, getData, setData, getOrder, setOrder, getInfo, 
    #           getSize, getName, setName, getKind
    # 필수 함수들은 반드시 존재해야 하며, 
    # editData를 제외하고는 파라미터와 리턴을 변경하면 안됨
    # 필요에 따라 내용을 추가할 수 있음

    def editData(self, name) :
        # 위젯의 특정 데이터를 수정
        self.name = str(name)
        #self.size_x = int(width)
        #self.size_y = int(height)
        # 입력되는 데이터에 따라 위젯을 조정
        #self.resize(self.size_x, self.size_y)

    def getData(self) : # 위젯의 데이터를 딕셔너리 형태로 리턴
        data = {}
        data["name"] = self.name
        data["order"] = self.order
        data["kind"] = self.kind
        data["size_x"] = self.size_x
        data["size_y"] = self.size_y
        data["is_connected"] = self.is_connected
        data["is_connecting"] = self.is_connecting

        data_widget = {}
        data_widget["image"] = self.get_image()

        data["etc"] = data_widget

        return data

    def setData(self, data) : # 딕셔너리 형태의 데이터로 위젯의 모든 데이터를 다시 설정
        self.name = data["name"]
        self.order = data["order"]
        #self.kind = data["kind"] # 재설정할 필요 없는 데이터
        #self.size_x = data["size_x"]
        #self.size_y = data["size_y"]
        self.is_connected = data["is_connected"]
        #self.is_connecting = data["is_connecting"] # 재설정할 필요 없는 데이터
        # 입력되는 데이터에 따라 위젯을 조정
        self.resize(self.size_x, self.size_y)
        self.set_image(data["etc"]["image"])

    def getOrder(self) : return self.order # order값을 리턴

    def setOrder(self, order) : self.order = int(order) # order값을 설정

    def getInfo(self) :
        info = "그림을 그릴 수 있는 그림판 위젯"
        return info

    def getSize(self) : return (self.size_x, self.size_y)

    def getName(self) : return self.name

    def setName(self, name) : self.name = str(name)

    def getKind(self) : return self.kind


    ######################## 연결 위젯 필수 함수 #########################
    # 다른 위젯의 기능을 이용할 수 있는 위젯이 필수적으로 가져야 하는 함수
    # 생성자 __init__이 실행된 이후 is_connecting이 true인 경우 이어서 실행됨
    # 파라미터로 연결할 위젯을 지정
    # 파라미터의 명칭이 연결할 위젯의 파일 이름과 같아야 함

    def setConnection(self) :
        pass

    def getConnection(self) :
        connected_widget = []
        return connected_widget


    ##################### 사용자 함수 작성 #########################
    # 위젯을 그릴 때 호출되는 함수
    def paintEvent(self, e):
        canvas = QPainter(self)
        canvas.drawImage(self.rect(), self.image, self.image.rect())

    # 마우스가 눌렸을 때 호출되는 함수
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = e.pos()

    # 마우스가 이벤트가 발생할 때 호출되는 함수
    def mouseMoveEvent(self, e):
        if (e.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine, Qt.RoundCap))
            painter.drawLine(self.last_point, e.pos())
            self.last_point = e.pos()
            self.update()

    # 마우스가 뗴어질 때 호출되는 함수
    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.drawing = False

    # 펜 사이즈 증가 함수
    def size_up(self):
        self.brush_size += 1

    # 펜 사이즈 감소 함수
    def size_down(self):
        if self.brush_size - 1 > 0:
            self.brush_size -= 1

    # 빨간 색으로 펜 색 변경
    def set_color_red(self):
        self.brush_color = Qt.red
    
    # 초록 색으로 펜 색 변경
    def set_color_green(self):
        self.brush_color = Qt.green

    # 파란 색으로 펜 색 변경
    def set_color_blue(self):
        self.brush_color = Qt.blue
        
    # 검은 색으로 펜 색 변경
    def set_color_black(self):
        self.brush_color = Qt.black
    
    # 현재 그림 저장
    def get_image(self) :
        ba = QByteArray()
        buf = QBuffer(ba)
        buf.open(QBuffer.WriteOnly)
        self.image.save(buf, "PNG")
        return (ba.data())

    # 저장한 그림 불러오기
    def set_image(self, img) :
        if img :
            self.image.fill(Qt.white)
            self.update()
            self.image.loadFromData(img)

    def clear_image(self) :
        self.image.fill(Qt.white)
        self.update()