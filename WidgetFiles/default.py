
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
    # 필수 함수 getData, setData, getOrder, setOrder, getSize, deleteWidget
    # 필수 함수들은 반드시 존재해야 하며, 파라미터를 변경하면 안됨
    # 필요에 따라 내용을 추가할 수 있음

    def getData(self) : # 위젯의 데이터를 리턴
        data = {}
        data["name"] = self.name
        data["order"] = self.order
        data["kind"] = self.kind
        data["is_connected"] = self.is_connected
        return data

    def setData(self, name) : # order를 제외한 위젯의 데이터 설정
        self.name = str(name)

    def getOrder(self) : return self.order # order값을 리턴

    def setOrder(self, order) : self.order = int(order) # order값을 설정

    def getInfo(self) :
        info = "위젯의 정보를 입력"
        return info

    def getSize(self, x, y) :
        # 위젯의 크기 값을 리턴
        return (self.size_x, self.size_y)

    def getName(self) : return self.name

    def setName(self, name) : self.name = str(name)

    def getKind(self) : return self.kind

    def deleteWidget(self) :
        # 상위 위젯에 위젯의 삭제 요청을 보냄
        pass


    ##################### 사용자 함수 작성 #########################