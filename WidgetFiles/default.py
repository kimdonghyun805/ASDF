
from PyQt5.QtWidgets import QWidget

class default (QWidget) :
    def __init__(self, name) : # 생성시 필요한 데이터를 생성자의 파라미터로 지정
        super().__init__()

        self.name = str(name) # 이 위젯 고유의 이름, 생성시 설정
        
        self.order = 0 # 위젯의 식별 번호, 각 위젯이 고유 값을 가짐, 생성시 설정, 변경 불가능

        # 위젯의 종류에 따라 사용자 임의로 설정, 실행 중 변경 불가능
        self.kind = "default" # 위젯의 종류, 위젯 파일의 이름
        self.size_x = 100 # 위젯의 가로 길이, 폭
        self.size_y = 100 # 위젯의 세로 길이, 높이

        # 위젯의 종류에 따라 사용자 임의로 설정, 실행 중 변경 가능
        self.is_connected = False # 위젯이 연결되었는지 확인
        self.is_connecting = False # 위젯이 연결 대상이 필요한지 확인

        self.resize(self.size_x, self.size_y) # 크기 설정

        ######################## 위젯 내용 작성 #######################


        ##################### 위젯 내용 작성 종료 #######################


    ######################### 필수 함수 #############################
    # 필수 함수 editData, getData, setData, getOrder, setOrder, getInfo, 
    #           getSize, getName, setName, getKind, deleteWidget
    # 필수 함수들은 반드시 존재해야 하며, 
    # editData를 제외하고는 파라미터와 리턴을 변경하면 안됨
    # 필요에 따라 내용을 추가할 수 있음

    def editData(self, name, x, y) :
        # 위젯의 특정 데이터를 수정
        self.name = str(name)
        self.size_x = int(x)
        self.size_y = int(y)
        # 입력되는 데이터에 따라 위젯을 조정
        self.resize(self.size_x, self.size_y)

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
        info = "위젯의 정보를 입력"
        return info

    def getSize(self) : return (self.size_x, self.size_y)

    def getName(self) : return self.name

    def setName(self, name) : self.name = str(name)

    def getKind(self) : return self.kind

    def deleteWidget(self) :
        # 상위 위젯에 위젯의 삭제 요청을 보냄
        pass

    ##################### 사용자 함수 작성 #########################