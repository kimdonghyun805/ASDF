import sys
 
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.Qt import *

class memo (QWidget) :
    def __init__(self, name, width, height) : # 생성시 필요한 데이터를 생성자의 파라미터로 지정
        super().__init__()

        self.name = str(name) # 이 위젯 고유의 이름, 생성시 설정
        
        self.order = 0 # 위젯의 식별 번호, 각 위젯이 고유 값을 가짐, 생성시 설정, 변경 불가능

        # 위젯의 종류에 따라 사용자 임의로 설정, 실행 중 변경 불가능
        self.kind = "memo" # 위젯의 종류, 위젯 파일의 이름
        self.size_x = int(width) # 위젯의 가로 길이, 폭
        self.size_y = int(height) # 위젯의 세로 길이, 높이

        # 위젯의 종류에 따라 사용자 임의로 설정, 실행 중 변경 가능
        self.is_connected = False # 위젯이 연결되었는지 확인
        self.is_connecting = False # 위젯이 연결 대상이 필요한지 확인
        self.list_widget_connected = [] # 연결하여 사용중인 위젯의 목록, 연결 위젯인 경우만 필요

        self.resize(self.size_x, self.size_y) # 크기 설정

        ######################## 위젯 내용 작성 #######################
        self.font = QFont("Arial", 10)
        self.font.setPixelSize(20)
        self.setStyleSheet("background-color : #FFFFFFFF")

        self.text_edit = QTextEdit(self)
        self.text_edit.resize(self.size_x, self.size_y)
        self.text_edit.move(0, 0)
        self.text_edit.setAcceptRichText(True)
        self.text_edit.setFont(self.font)
        self.text_edit.setStyleSheet("background-color : #FFFFFFFF")

        ##################### 위젯 내용 작성 종료 #######################


    ######################### 필수 함수 #############################
    # 필수 함수 editData, getData, setData, getOrder, setOrder, getInfo, 
    #           getSize, getName, setName, getKind
    # 필수 함수들은 반드시 존재해야 하며, 
    # editData를 제외하고는 파라미터와 리턴을 변경하면 안됨
    # 필요에 따라 내용을 추가할 수 있음

    def editData(self, name, width, height) :
        # 위젯의 특정 데이터를 수정
        self.name = str(name)
        self.size_x = int(width)
        self.size_y = int(height)
        # 입력되는 데이터에 따라 위젯을 조정
        self.resize(self.size_x, self.size_y)
        self.text_edit.resize(self.size_x, self.size_y)

    def getData(self) : # 위젯의 데이터를 딕셔너리 형태로 리턴
        data = {}
        data["name"] = self.name
        data["order"] = self.order
        data["kind"] = self.kind
        data["size_x"] = self.size_x
        data["size_y"] = self.size_y
        data["is_connected"] = self.is_connected
        data["is_connecting"] = self.is_connecting

        data_memo = {}
        data_memo["text"] = self.text_edit.toPlainText()
        data["etc"] = data_memo

        return data

    def setData(self, data) : # 딕셔너리 형태의 데이터로 위젯의 모든 데이터를 다시 설정
        self.name = data["name"]
        self.order = data["order"]
        #self.kind = data["kind"] # 재설정할 필요 없는 데이터
        self.size_x = data["size_x"]
        self.size_y = data["size_y"]
        self.is_connected = data["is_connected"]
        #self.is_connecting = data["is_connecting"] # 재설정할 필요 없는 데이터
        
        data_memo = data["etc"]
        text = data_memo["text"]
        
        # 입력되는 데이터에 따라 위젯을 조정
        self.resize(self.size_x, self.size_y)
        self.setText(text)

    def getOrder(self) : return self.order # order값을 리턴

    def setOrder(self, order) : self.order = int(order) # order값을 설정

    def getInfo(self) :
        info = "텍스트를 표시하는 메모장 위젯\n"
        info = info + "위젯 생성 시 크기(width, height) 입력"
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

    def set_text(self, text) :
        self.text_edit.setText(text)

    def get_text(self) :
        text = self.text_edit.toPlainText()
        return text

    def clear_text(self) :
        self.text_edit.setText("")