import Header

class Programming(Header.QWidget) :
    def __init__(self, size_x, size_y, dictionary_icon, font, path_savefiles) :
        super().__init__()
        self.size_x = size_x
        self.size_y = size_y
        
        self.icon_move = dictionary_icon["move"]
        self.icon_edit = dictionary_icon["edit"]
        self.icon_close = dictionary_icon["close"]

        self.font = font
        self.path_savefiles = path_savefiles

        self.order = 0

        self.resize(Header.QSize(self.size_x, self.size_y))
        self.setFixedSize(self.size_x, self.size_y)

        self.widget = Header.QWidget(self)
        self.widget.resize(Header.QSize(self.size_x - 20, self.size_y - 20))
        self.setFixedSize(self.size_x - 20, self.size_y - 20)
        self.widget.move(0, 0)

        self.widget.setStyleSheet("border-style : solid; border-width : 2px; border-color : #00FF00;")
        self.title = Header.QLabel("Programming", self.widget)
        self.title.setFont(self.font)
        self.title.move(10, 10)

        self.size_x_dialog_default = 300
        self.size_y_dialog_default = 0
        self.size_x_dialog = 300
        self.size_y_dialog = 0
        self.need_to_set_parameter = False
        self.dict_parm_dialog = {}
        self.dialog_parameter = self.makeParameterDialog()
        

    def makeParameterDialog(self) :
        list_input_value = [] # 입력값을 저장할 리스트

        dialog = Header.QDialog(None, Header.Qt.WindowTitleHint | Header.Qt.WindowCloseButtonHint)
        dialog.setWindowTitle("위젯 정보 입력")
        dialog.setFixedWidth(self.size_x_dialog_default)
        dialog.setFixedHeight(self.size_y_dialog_default)

        return dialog

    def appendParameterDialog(self, name) :
        # 다이얼로그 길이 조정
        size_y_label = 40
        self.size_y_dialog = self.size_y_dialog + size_y_label
        self.dialog_parameter.setFixedHeight(self.size_y_dialog)

        label_name = Header.QLabel(name, self.dialog_parameter)
        label_name.setFont(self.font)
        label_name.setFixedSize(120, 30)
        label_name.setAlignment(Header.Qt.AlignRight)
        label_input = Header.QLineEdit("", self.dialog_parameter)
        label_input.setFont(self.font)
        label_input.setFixedSize(120, 30)

        label_name.move(10, self.size_y_dialog - size_y_label + 5)
        label_input.move(160, self.size_y_dialog - size_y_label + 5)

        self.dict_parm_dialog[name] = label_input

    def appendParameterDialogButton(self) :
        size_y_button = 40
        self.size_y_dialog = self.size_y_dialog + size_y_button
        self.dialog_parameter.setFixedHeight(self.size_y_dialog)

        button_ok = Header.QPushButton("확인", self.dialog_parameter)
        button_ok.setFont(self.font)
        button_ok.setFixedSize(100, 30)
        button_ok.move(70, self.size_y_dialog - size_y_button + 5)
        button_ok.clicked.connect(lambda : self.clickedDialogOk(True))

        button_cancel = Header.QPushButton("취소", self.dialog_parameter)
        button_cancel.setFont(self.font)
        button_cancel.setFixedSize(100, 30)
        button_cancel.move(180, self.size_y_dialog - size_y_button + 5)
        button_cancel.clicked.connect(self.dialog_parameter.close)

    def clearParameterDialog(self) : # 다이얼로그 초기화
        del(self.dialog_parameter)
        self.dialog_parameter = self.makeParameterDialog()
        self.size_x_dialog = self.size_x_dialog_default
        self.size_y_dialog = self.size_y_dialog_default

        del(self.dict_parm_dialog)
        self.dict_parm_dialog = {}

    def clickedDialogOk(self, t_or_f) :
        self.need_to_set_parameter = t_or_f
        self.dialog_parameter.close()

    def checkParameters(self, data_widgetfiles) :
        # widget list 에서 위젯 생성 버튼 입력시 실행
        # 위젯 파일의 정보를 받아 위젯 객체 생성
        #print("do checkParameter")
        #print("widget file :", data_widgetfiles)

        # 위젯의 클래스 정보 - 객체 생성을 위함
        class_widget = data_widgetfiles["class"]

        # 생성자의 파라미터 확인
        func_init = data_widgetfiles["function"]["__init__"]
        parm_init = Header.inspect.signature(func_init).parameters.values()

        # 입력받아야 하는 파라미터 추출
        list_parm_name = [] # 설정해야 하는 모든 파라미터 리스트
        list_parm_input = [] # 입력해야 하는 파라미터 리스트
        list_parm_value = [] # 입력한 파라미터 값이 저장될 리스트
        for parm in parm_init :
            if parm.default == Header.inspect._empty :
                name = parm.name
                list_parm_name.append(name)
                if (name != "self") and (name != "order") :
                    list_parm_input.append(name)

        #print("list_parm_name :", list_parm_name)
        #print("list_parm_input :", list_parm_input)

        # 다이얼로그 비우기
        self.clearParameterDialog()
        if list_parm_input : # 입력할 파라미터가 있는 경우
            # 다이얼로그로 파라미터를 입력받아 파라미터 리스트 제작
            for parm in list_parm_input : # 입력할 파라미터 추가
                self.appendParameterDialog(parm)

            # 다이얼로그에 확인 버튼 추가 후 실행
            self.appendParameterDialogButton()
            self.dialog_parameter.exec_()
            #print("dict_parm_dialog :", self.dict_parm_dialog)

            if self.need_to_set_parameter : # 확인 버튼이 입력된 경우
                for parm in list_parm_name : # 파라미터 정보를 변환
                    if parm == "self" :
                        pass
                    elif parm == "order" :
                        self.order = self.order + 1
                        list_parm_value.append(self.order)
                    else :
                        value = self.dict_parm_dialog[parm].text()
                        list_parm_value.append(value)

                self.need_to_set_parameter = False

                #print("list_parm_input :", list_parm_input)
                #print("list_parm_value :", list_parm_value)
                self.createWidget(class_widget, list_parm_value)

        else :
            # 입력할 파라미터가 없는 경우, 그대로 위젯 생성
            self.createWidget(class_widget, list_parm_value)

 
    def createWidget(self, class_widget, list_parm_value) :
        # 위젯의 객체를 생성
        # list_parm_value에는 self를 제외한 모든 파라미터를 순서대로 가져야 함
        # 위젯 프레임(이름, 이동, 수정, 삭제 버튼) 제작
        # 위젯 프레임에 위젯 객체를 올리고 화면에 표시
        print("do createWidget")
        print("list_parm_value :", list_parm_value)
        try :
            obj = class_widget(*list_parm_value)
        except :
            # 잘못된 파라미터 값이 지정된 경우, 오류 발생
            print("maybe input wrong value for parameter...")
            return

        print("create widget object :", obj)
        
        obj.setParent(self.widget)
        #self.widget.child
        obj.move(50, 50)
        self.widget.show()
        obj.show()