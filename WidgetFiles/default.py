
from PyQt5.QtWidgets import QWidget

class default (QWidget) :
    def __init__(self, name, order) :
        super.__init__()

        self.name = "" # 이 위젯 고유의 이름, 생성시 설정
        
        self.order = 0 # 위젯의 식별 번호, 각 위젯이 고유 값을 가짐, 생성시 설정, 변경 불가능

        # 위젯의 종류에 따라 사용자 임의로 설정, 실행 중 변경 불가능
        self.kind = "default" # 위젯의 종류, 위젯 파일의 이름
        self.size_x = 100 # 위젯의 가로 길이, 폭
        self.size_y = 100 # 위젯의 세로 길이, 높이

        # 위젯의 종류에 따라 사용자 임의로 설정, 실행 중 변경 가능
        self.is_connected = False # 위젯이 연결되었는지 확인
        self.is_connecting = False # 위젯이 연결 대상이 필요한지 확인


    def getData(self) : # 위젯의 데이터를 리턴
        data = {}
        data["name"] = self.name
        data["order"] = self.order
        data["kind"] = self.kind
        data["is_connected"] = self.is_connected
        return data

    def setData(self, data) : # 위젯의 데이터 설정
        self.name = data["name"]
        self.order = data["order"]
        self.kind = data["kind"]
        self.is_connected = data["is_connected"]

    def getOrder(self) : return self.order # order값을 리턴

    def setOrder(self, order) : self.order = order # order값을 설정

    def getInfo(self) :
        info = "위젯의 정보를 입력"
        return info

    def setLocation(self, x, y) :
        # 위젯의 위치를 x, y 이동
        pass

    def deleteWidget(self) :
        # 상위 위젯에 위젯의 삭제 요청을 보냄
        pass