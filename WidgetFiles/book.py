import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class book (QWidget) :
    def __init__(self, name) : # 생성시 필요한 데이터를 생성자의 파라미터로 지정
        super().__init__()

        self.name = str(name) # 이 위젯 고유의 이름, 생성시 설정
        
        self.order = 0 # 위젯의 식별 번호, 각 위젯이 고유 값을 가짐, 생성시 설정, 변경 불가능

        # 위젯의 종류에 따라 사용자 임의로 설정, 실행 중 변경 불가능
        self.kind = "book" # 위젯의 종류, 위젯 파일의 이름
        self.size_x = 200 # 위젯의 가로 길이, 폭
        self.size_y = 80 # 위젯의 세로 길이, 높이

        # 위젯의 종류에 따라 사용자 임의로 설정, 실행 중 변경 가능
        self.is_connected = False # 위젯이 연결되었는지 확인
        self.is_connecting = True # 위젯이 연결 대상이 필요한지 확인
        self.list_widget_connected = [] # 연결하여 사용중인 위젯의 목록, 연결 위젯인 경우만 필요

        self.resize(self.size_x, self.size_y) # 크기 설정

        ######################## 위젯 내용 작성 #######################
        self.font = QFont("Arial", 10, QFont.Bold)
        self.font.setPixelSize(14)
        self.setStyleSheet("background-color : #FFFFFFFF")

        self.max_page = 0
        self.now_page = 0
        self.widget_memo = None
        self.widget_paint = None
        self.book_data = []

        self.label = QLabel("", self)
        self.label.setFont(self.font)
        self.label.resize(120, 30)
        self.label.move(40, 10)
        self.label.setAlignment(Qt.AlignCenter)

        self.new_btn = QPushButton("새 페이지",self)
        self.new_btn.clicked.connect(self.new_page)
        self.new_btn.setFont(self.font)
        self.new_btn.resize(100, 30)
        self.new_btn.move(50, 40)

        self.prev_btn = QPushButton("이전",self)
        self.prev_btn.clicked.connect(self.prev_page)
        self.prev_btn.setFont(self.font)
        self.prev_btn.resize(50, 30)
        self.prev_btn.move(10, 40)

        self.next_btn = QPushButton("다음",self)
        self.next_btn.clicked.connect(self.next_page)
        self.next_btn.setFont(self.font)
        self.next_btn.resize(50, 30)
        self.next_btn.move(140, 40)


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

        list_connection = []
        dict_memo = {}
        dict_memo["name"] = self.widget_memo.getName()
        dict_memo["kind"] = self.widget_memo.getKind()
        list_connection.append(dict_memo)
        dict_paint["name"] = self.widget_paint.getName()
        dict_paint["kind"] = self.widget_paint.getKind()
        list_connection.append(dict_paint)
        data["connection"] = list_connection

        data["etc"] = self.book_data
        return data

    def setData(self, data) : # 딕셔너리 형태의 데이터로 위젯의 모든 데이터를 다시 설정
        self.name = data["name"]
        self.order = data["order"]
        #self.kind = data["kind"] # 재설정할 필요 없는 데이터
        #self.size_x = data["size_x"]
        #self.size_y = data["size_y"]
        self.is_connected = data["is_connected"]
        #self.is_connecting = data["is_connecting"] # 재설정할 필요 없는 데이터

        # 위젯의 연결은 저장 데이터를 불러오는 함수에서 설정

        self.book_data = data["etc"]
        self.max_page = len(self.book_data)

        # 입력되는 데이터에 따라 위젯을 조정
        #self.resize(self.size_x, self.size_y)
        self.now_page = -1
        self.next_page()

    def getOrder(self) : return self.order # order값을 리턴

    def setOrder(self, order) : self.order = int(order) # order값을 설정

    def getInfo(self) :
        info = "그림과 그에 대한 설명을 가진 도감 위젯\n"
        info = info + "memo와 paint 위젯의 연결이 필요함"
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

    def setConnection(self, memo, paint) :
        self.widget_memo = memo
        self.widget_paint = paint
        self.new_page()

    def getConnection(self) :
        connected_widget = []
        connected_widget.append(self.widget_memo)
        connected_widget.append(self.widget_paint)
        return connected_widget


    ##################### 사용자 함수 작성 #########################
    def prev_page(self) :
        if self.now_page - 1 >= 0 : # 이전 페이지가 존재해야 함
            # 현재 페이지 정보 저장
            self.save_page()

            # 이전 페이지 표시
            self.now_page -= 1
            self.widget_memo.set_text(self.book_data[self.now_page]["memo"])
            self.widget_paint.set_image(self.book_data[self.now_page]["paint"])
            self.set_label_page(self.now_page)
        else : # 다음 페이지가 존재하지 않는 경우, 이무것도 하지 않음
            print("not have prev page")
            pass 

    def next_page(self) :
        if self.now_page + 1 < self.max_page : # 다음 페이지가 존재해야 함
            # 현재 페이지 정보 저장
            self.save_page()

            # 다음 페이지 표시
            self.now_page += 1
            self.widget_memo.set_text(self.book_data[self.now_page]["memo"])
            self.widget_paint.set_image(self.book_data[self.now_page]["paint"])
            self.set_label_page(self.now_page)
        else : # 다음 페이지가 존재하지 않는 경우, 이무것도 하지 않음
            print("not have next page")
            pass 

    def new_page(self) :
        if self.max_page != 0 :
            self.save_page()

        self.max_page = self.max_page + 1
        self.now_page = self.max_page - 1
        
        self.widget_memo.clear_text()
        self.widget_paint.clear_image()
        
        page_data = {}
        page_data["memo"] = self.widget_memo.get_text()
        page_data["paint"] = self.widget_paint.get_image()
        
        self.book_data.append(page_data)
        self.set_label_page(self.now_page)

    def set_label_page(self, page) :
        s = "현재 페이지 : " + str(page + 1)
        self.label.setText(s)

    def save_page(self) :
        if self.now_page in range(0, self.max_page) :
            self.book_data[self.now_page]["memo"] = self.widget_memo.get_text()
            self.book_data[self.now_page]["paint"] = self.widget_paint.get_image()