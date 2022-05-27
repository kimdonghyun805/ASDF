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
        self.title.move(0, 0)

        self.size_x_dialog_default = 300
        self.size_y_dialog_default = 0
        self.size_x_dialog = 300
        self.size_y_dialog = 0
        self.need_to_set_parameter = False
        self.dict_parm_dialog = {}
        self.dialog_parameter = self.makeParameterDialog()
    
        self.dialog_error, self.label_error_message = self.makeErrorDialog()

        self.list_widget = []
        self.list_frame = [] # [ {frame, label, order}, ... ]
        self.list_data_widget = []
        self.num_widget = 0

    def makeErrorDialog(self) :
        dialog = Header.QDialog(None, Header.Qt.WindowTitleHint | Header.Qt.WindowCloseButtonHint)
        dialog.setWindowTitle("오류")
        dialog.setFixedSize(300, 120)

        label_message = Header.QLabel("", dialog)
        label_message.setFont(self.font)
        label_message.setFixedSize(260, 40)
        label_message.move(20, 20)

        button_close = Header.QPushButton("닫기", dialog)
        button_close.setFont(self.font)
        button_close.setFixedSize(100, 30)
        button_close.move(180, 80)
        button_close.clicked.connect(dialog.close)

        return dialog, label_message

    def showErrorDialog(self, error_no) :
        # error_no
        # 1 : 잘못된 파라미터 인식
        # 2 : 위젯 생성 제한 초과
        message = ""
        if (error_no == 1) :
            message = "위젯 파일에 오류가 있거나\n잘못된 데이터가 입력되었습니다."
        elif (error_no == 2) :
            message = "더 이상 위젯을 생성할 수 없습니다."
        else :
            message = "알수 없는 오류가 발생했습니다."

        self.label_error_message.setText(message)
        self.dialog_error.exec_()


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

        if self.num_widget >= 10 :
            self.showErrorDialog(2)
            return

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
                        if not value : value = 0
                        list_parm_value.append(value)
                self.need_to_set_parameter = False
                # 입력된 파라미터에 따라 위젯 생성
                self.createWidget(class_widget, list_parm_value)

        else : # 파라미터가 self 혹은 self, order 뿐인 경우
            if "order" in list_parm_name :
                self.order = self.order + 1
                list_parm_value.append(self.order)
                # 입력된 파라미터에 따라 위젯 생성
                self.createWidget(class_widget, list_parm_value)

        # 입력된 파라미터에 따라 위젯 생성
        #self.createWidget(class_widget, list_parm_value)

 
    def createWidget(self, class_widget, list_parm_value) :
        # 위젯의 객체를 생성
        # list_parm_value에는 self를 제외한 모든 파라미터를 순서대로 가져야 함
        # 위젯 프레임(이름, 이동, 수정, 삭제 버튼) 제작
        # 위젯 프레임에 위젯 객체를 올리고 화면에 표시
        # 프레임이 아닌 위젯 객체를 리스트 list_widget에 저장
        print("do createWidget")
        print("list_parm_value :", list_parm_value)
        object_widget = None
        try :
            if list_parm_value :
                object_widget = class_widget(*list_parm_value)
            else :
                object_widget = class_widget()
            if object_widget.getOrder() == 0 : # 생성시 order가 지정되지 않은 경우
               self.order = self.order + 1
               object_widget.setOrder(self.order)
               #print("set order :", self.order)
        except :
            # 잘못된 파라미터 값이 지정된 경우, 오류 발생
            self.showErrorDialog(1)
            return

        print("create widget object :", object_widget)
        print("widget order :", object_widget.order)
        
        self.list_widget.append(object_widget)
        self.num_widget = self.num_widget + 1

        # 위젯을 표시하고 버튼을 표시할 프레임 제작
        data_frame = self.makeWidgetFrame(object_widget)
        data_frame["order"] = object_widget.getOrder()
        self.list_frame.append(data_frame)

        frame_widget = data_frame["frame"]
        self.list_frame.append(frame_widget)
        #frane_widget.setParent(self.widget)

        object_widget.setParent(frame_widget)
        object_widget.move(5, 30)
        loc_x, loc_y = self.setInitialLocation()
        frame_widget.move(loc_x, loc_y)
        #self.widget.show()
        frame_widget.show()
        #object_widget.show()

        print("list_widget :", self.list_widget)

    def makeWidgetFrame(self, object) :
        data_frame = {}

        frame = Header.QWidget(self.widget)
        (x, y) = object.getSize()
        frame.setFixedSize(x + 10, y + 30)
        frame.setStyleSheet("background-color : white;")
        
        label_name = Header.QLabel(object.getName(), frame)
        label_name.setFont(self.font)
        label_name.move(5, 5)

        button_move = Header.QPushButton("", frame)
        button_move.setIcon(self.icon_move)
        button_move.setIconSize(Header.QSize(20, 20))
        button_move.move(x - 85, 5)
        button_move.clicked.connect(self.moveWidget)

        button_edit = Header.QPushButton("", frame)
        button_edit.setIcon(self.icon_edit)
        button_edit.setIconSize(Header.QSize(20, 20))
        button_edit.move(x - 55, 5)
        button_edit.clicked.connect(self.editWidgetData)

        button_close = Header.QPushButton("", frame)
        button_close.setIcon(self.icon_close)
        button_close.setIconSize(Header.QSize(20, 20))
        button_close.move(x - 25, 5)
        button_close.clicked.connect(self.closeWidget)

        data_frame["frame"] = frame
        data_frame["name"] = label_name
        return data_frame

    def setInitialLocation(self) :
        x = Header.random.randint(10, 60)
        y = Header.random.randint(10, 70)
        return x, y

    def moveWidget(self) :
        print("do moveWidget")

    def editWidgetData(self) :
        print("do editWidgetData")

    def closeWidget(self) :
        print("do closeWidget")