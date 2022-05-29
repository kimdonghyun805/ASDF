from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel

class test_connect (QWidget) :
    def __init__(self, name) : # 생성시 필요한 데이터를 생성자의 파라미터로 지정
        super().__init__()

        self.name = str(name) # 이 위젯 고유의 이름, 생성시 설정
        
        self.order = 0 # 위젯의 식별 번호, 각 위젯이 고유 값을 가짐, 생성시 설정, 변경 불가능

        # 위젯의 종류에 따라 사용자 임의로 설정, 실행 중 변경 불가능
        self.kind = "test_connect" # 위젯의 종류, 위젯 파일의 이름
        self.size_x = 200 # 위젯의 가로 길이, 폭
        self.size_y = 150 # 위젯의 세로 길이, 높이

        # 위젯의 종류에 따라 사용자 임의로 설정, 실행 중 변경 가능
        self.is_connected = False # 위젯이 연결되었는지 확인
        self.is_connecting = True # 위젯이 연결 대상이 필요한지 확인

        self.resize(self.size_x, self.size_y) # 크기 설정

        ######################## 위젯 내용 작성 #######################
        print("A1")
        self.index = 0
        self.memo_widget = None
        self.paint_widget = None
        self.list_widget_data = []
        print("A2")
        self.widget = QWidget(self)
        self.widget.resize(self.size_x, self.size_y)
        print("A3")
        self.label = QLabel(str(self.index), self.widget)
        self.label.resize(self.size_x - 40, self.size_y - 100)
        self.label.move(20, 20)
        self.label.setAlignment(Qt.AlignCenter)
        print("A4")
        self.next_button = QPushButton("prev", self.widget)
        self.next_button.resize(40, 40)
        self.next_button.move(20, 80)
        self.next_button.clicked.connect(self.prevIndex)
        print("A5")
        self.prev_button = QPushButton("next", self.widget)
        self.prev_button.resize(40, 40)
        self.prev_button.move(140, 80)
        self.prev_button.clicked.connect(self.nextIndex)
        print("A6")
        self.save_button = QPushButton("SaveNow", self.widget)
        self.save_button.resize(40, 40)
        self.save_button.move(80, 80)
        self.save_button.clicked.connect(self.saveWidgetData)
        print("A7")

        ##################### 위젯 내용 작성 종료 #######################


    ######################### 필수 함수 #############################
    # 필수 함수 editData, getData, setData, getOrder, setOrder, getInfo, 
    #           getSize, getName, setName, getKind, deleteWidget
    # 필수 함수들은 반드시 존재해야 하며, 
    # editData를 제외하고는 파라미터와 리턴을 변경하면 안됨
    # 필요에 따라 내용을 추가할 수 있음

    def editData(self, name) :
        # 위젯의 특정 데이터를 수정
        self.name = str(name)
        # 입력되는 데이터에 따라 위젯을 조정

    def getData(self) : # 위젯의 데이터를 딕셔너리 형태로 리턴
        data = {}
        data["name"] = self.name
        data["order"] = self.order
        data["kind"] = self.kind
        data["size_x"] = self.size_x
        data["size_y"] = self.size_y
        data["is_connected"] = self.is_connected
        data["is_connecting"] = self.is_connecting
        return data

    def setData(self, data) : # 딕셔너리 형태의 데이터로 위젯의 모든 데이터를 다시 설정
        self.name = data["name"]
        self.order = data["order"]
        #self.kind = data["kind"] # 재설정할 필요 없는 데이터
        self.size_x = data["size_x"]
        self.size_y = data["size_y"]
        self.is_connected = data["is_connected"]
        #self.is_connecting = data["is_connecting"] # 재설정할 필요 없는 데이터
        # 입력되는 데이터에 따라 위젯을 조정
        self.resize(self.size_x, self.size_y)

    def getOrder(self) : return self.order # order값을 리턴

    def setOrder(self, order) : self.order = int(order) # order값을 설정

    def getInfo(self) :
        info = "connect 테스트용 위젯\n생성시 name 입력\n위젯 memo, paint 연결 필요"
        return info

    def getSize(self) : return (self.size_x, self.size_y)

    def getName(self) : return self.name

    def setName(self, name) : self.name = str(name)

    def getKind(self) : return self.kind

    def deleteWidget(self) :
        # 상위 위젯에 위젯의 삭제 요청을 보냄
        pass

    ##################### 사용자 함수 작성 #########################
    def connectWidget(self, memo, paint) :
        self.memo_widget = memo
        self.paint_widget = paint
        print("do connectWidget :", self.memo_widget, self.paint_widget)

    def saveWidgetData(self) :
        if (self.memo_widget is None) or (self.paint_widget is None) :
            print("Need to connecting widgets")
        else :
            memo_data = self.memo_widget.getData()
            self.list_widget_data.append(memo_data)
            paint_data = self.paint_widget.getData()
            self.list_widget_data.append(paint_data)

    def nextIndex(self) :
        self.index = self.index + 1
        self.label.setText(str(self.index))

    def prevIndex(self) :
        self.index = self.index - 1
        self.label.setText(str(self.index))
        