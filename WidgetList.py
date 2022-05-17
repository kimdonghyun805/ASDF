import Header

class WidgetList (Header.QScrollArea) :
    def __init__(self, size_x, size_y, dictionary_icon, font, widget) :
        super().__init__(widget)
        self.size_x = size_x
        self.size_y = size_y

        self.icon_info = dictionary_icon["info"]
        self.icon_edit = dictionary_icon["edit"]
        self.icon_add = dictionary_icon["add"]

        self.font = font
        print("widget list font :", self.font.toString())

        self.height_widget_file = 110
        self.now_height_widget = 20

        self.resize(Header.QSize(self.size_x, self.size_y))
        self.setFixedWidth(self.size_x)
        self.setFixedHeight(self.size_y)

        self.setVerticalScrollBarPolicy(Header.Qt.ScrollBarAlwaysOn)
        self.setWidgetResizable(False)
        self.setEnabled(True)

        self.widget = Header.QWidget()
        self.widget.resize(Header.QSize(self.size_x - 22, 0))
        self.widget.setFixedWidth(self.size_x - 22)
        #self.widget.setMinimumHeight(self.size_y - 4)

        self.setWidget(self.widget)

        self.layout = Header.QVBoxLayout()
        self.widget.setLayout(self.layout)

        self.setStyleSheet("border-style : solid; border-width : 2px; border-color : #FF0000;")
        self.setVisible(True)

        for n in range(1, 11) :
            self.d = self.makeWidgetFile(str(n)*15)
            self.layout.addWidget(self.d)
            self.setWidgetHeight(True, self.height_widget_file)


    def setWidgetHeight(self, up_or_down, height) :
        if up_or_down :
            # true인 경우 up - 높이 증가
            self.now_height_widget = self.now_height_widget + height + 10
        else :
            # false인 경우 down - 높이 감소
            if now_height_widget >= 0 :
                self.now_height_widget = self.now_height_widget - height - 10
        self.widget.setFixedHeight(self.now_height_widget)


    def makeWidgetFile(self, name) :
        widget_file = Header.QGroupBox()
        width = 200
        height = 110
        widget_file.resize(Header.QSize(width, height))
        widget_file.setFixedSize(width, height)

        widget_name = Header.QLabel(name, widget_file)
        widget_name.setFont(self.font)
        widget_name.setFixedWidth(163)
        widget_name.setFixedHeight(35)
        widget_name.setAlignment(Header.Qt.AlignLeft)
        widget_name.move(20, 20)
        
        button_info = Header.QPushButton(None, widget_file)
        button_info.setIcon(self.icon_info)
        button_info.setIconSize(Header.QSize(35, 35))
        button_info.move(20, 60)
        button_info.setToolTip("이 위젯의 정보를 표시합니다.")
        button_info.clicked.connect(lambda : self.displayWidgetInfo())

        button_edit = Header.QPushButton(None, widget_file)
        button_edit.setIcon(self.icon_edit)
        button_edit.setIconSize(Header.QSize(35, 35))
        button_edit.move(80, 60)
        button_edit.setToolTip("이 위젯 파일의 내용을 수정합니다.")
        button_edit.clicked.connect(lambda : self.editWidgetFile())

        button_add = Header.QPushButton(None, widget_file)
        button_add.setIcon(self.icon_add)
        button_add.setIconSize(Header.QSize(35, 35))
        button_add.move(140, 60)
        button_add.setToolTip("이 위젯을 사용하기 위해 생성합니다.")
        button_add.clicked.connect(lambda : self.makeWidget())

        widget_file.setStyleSheet("border-style : solid; border-width : 2px; border-color : #000000;")
        return widget_file
        
    def displayWidgetInfo(self) :
        print("do displayWidgetInfo")

    def editWidgetFile(self) :
        print("do editWidgetFile")

    def makeWidget(self) :
        print("do makeWidget")

    def checkWidgetFile(self) :
        # 폴더 위치에서 위젯 파일들을 확인
        pass

    def displayWidgetFileList(self) :
        # 확인한 위젯 파일들의 목록을 위젯 형태로 만들어 표시함
        pass