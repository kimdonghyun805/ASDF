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
        self.setAcceptDrops(True)

        self.resize(Header.QSize(self.size_x, self.size_y))
        self.setFixedSize(self.size_x, self.size_y)

        self.widget = Header.QWidget(self)
        self.widget.resize(Header.QSize(self.size_x - 20, self.size_y - 20))
        self.setFixedSize(self.size_x - 20, self.size_y - 20)
        self.widget.move(0, 0)
        #self.widget.setAcceptDrops(True)

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
    
        self.dialog_error = self.makeErrorDialog()

        self.list_widget = []
        self.list_frame = []
        self.list_data_widget = []
        self.num_widget = 0

    def makeErrorDialog(self) :
        dialog = Header.QDialog(None, Header.Qt.WindowTitleHint | Header.Qt.WindowCloseButtonHint)
        dialog.setWindowTitle("오류")
        dialog.setFixedSize(300, 120)

        label_message = Header.QLabel("", dialog)
        label_message.setFont(self.font)
        label_message.setFixedSize(260, 70)
        label_message.move(20, 10)

        button_close = Header.QPushButton("닫기", dialog)
        button_close.setFont(self.font)
        button_close.setFixedSize(100, 30)
        button_close.move(180, 80)
        button_close.clicked.connect(dialog.close)

        return dialog

    def showErrorDialog(self, error_no) :
        # error_no
        # 1 : 잘못된 파라미터 인식
        # 2 : 위젯 생성 제한 초과
        # 3 : 위젯 데이터 수정시 잘못된 데이터 입력
        # 4 : 위젯에 연결 정보 확인 변수(is_connecting, is_connected) 가 없음
        message = ""
        if (error_no == 1) :
            message = "위젯 파일에 오류가 있거나\n잘못된 데이터가 입력되었습니다."
        elif (error_no == 2) :
            message = "더 이상 위젯을 생성할 수 없습니다."
        elif (error_no == 3) :
            message = "위젯의 데이터 수정기능에\n오류가 있거나 잘못된 데이터가\n입력되었습니다."
        elif (error_no == 4) :
            message = "위젯의 특정 데이터가 손실되어 있습니다."
        else :
            message = "알수 없는 오류가 발생했습니다."

        #self.label_error_message.setText(message)
        #print("child :", self.dialog_error.findChild(Header.QLabel))
        label = self.dialog_error.findChild(Header.QLabel)
        label.setText(message)
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
        # 위젯 파일의 정보를 받아 위젯 객체 생성에 필요한 정보 추출
        if self.num_widget >= 10 :
            self.showErrorDialog(2)
            return

        # 위젯의 클래스 정보 - 객체 생성을 위함
        class_widget = data_widgetfiles["class"]

        # 생성자의 파라미터 확인
        func_init = data_widgetfiles["function"]["__init__"]
        func_edit_data = data_widgetfiles["function"]["editData"]
        #print("func_edit_data :", type(func_edit_data), func_edit_data)
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

        # 다이얼로그 비우기
        self.clearParameterDialog()
        if list_parm_input : # 입력할 파라미터가 있는 경우
            # 다이얼로그로 파라미터를 입력받아 파라미터 리스트 제작
            for parm in list_parm_input : # 입력할 파라미터 추가
                self.appendParameterDialog(parm)

            # 다이얼로그에 확인 버튼 추가 후 실행
            self.appendParameterDialogButton()
            self.dialog_parameter.exec_()

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
                self.createWidget(class_widget, list_parm_value, func_edit_data)

        else : # 파라미터가 self 혹은 self, order 뿐인 경우
            if "order" in list_parm_name :
                self.order = self.order + 1
                list_parm_value.append(self.order)
                # 입력된 파라미터에 따라 위젯 생성
                self.createWidget(class_widget, list_parm_value, func_edit_data)
 
    def createWidget(self, class_widget, list_parm_value, func_edit) :
        # 위젯의 객체를 생성
        object_widget = None
        try :
            if list_parm_value :
                object_widget = class_widget(*list_parm_value)
            else :
                object_widget = class_widget()
            if object_widget.getOrder() == 0 : # 생성시 order가 지정되지 않은 경우
                self.order = self.order + 1
                object_widget.setOrder(self.order)
        except :
            # 잘못된 파라미터 값이 지정된 경우, 오류 발생
            self.showErrorDialog(1)
            return

        # 연결 대상이 필요한 경우를 확인하고 지정함 - 작성중
        try :
            if object_widget.is_connecting :
                print("widget need connecting")
        except :
            #위젯에 is_connecting, is_connected 변수가 없는 경우
            self.showErrorDialog(4)
            return
        
        self.list_widget.append(object_widget)
        self.num_widget = self.num_widget + 1

        # 위젯과 버튼을 표시할 프레임 제작
        frame = self.makeWidgetFrame(object_widget, func_edit)
        self.list_frame.append(frame)
        
        loc_x, loc_y = self.setInitialLocation()
        frame.move(loc_x, loc_y)
        frame.show()

    def makeWidgetFrame(self, object, func_edit) :
        (x, y) = object.getSize()
        frame = WidgetFrame(x, y, object.getOrder(), self.font, self.icon_move, self.icon_edit, self.icon_close)
        frame.setParent(self.widget)
        frame.setWidget(object)
        frame.setEditFunction(func_edit)
        #frame.setName(object.getName())
        frame.signal_edit_widget.connect(self.editWidgetData)
        frame.signal_close_widget.connect(self.closeWidget)
        object.move(5, 30)

        return frame

    def editWidgetData(self, order) :
        # 위젯의 일부 데이터 수정 - 위젯의 editData 호출
        print("do editWidgetData at Programming")
        frame = None
        for f in self.list_frame :
            if f.order == order :
                frame = f
        if not frame :
            print("Widget could not be found through order")
            return
        print("find widget :", frame.label_name.text())
        parm_edit = Header.inspect.signature(frame.func_edit).parameters.values()

        # 입력받아야 하는 파라미터 추출
        list_parm_name = [] # 설정해야 하는 모든 파라미터 리스트
        list_parm_input = [] # 입력해야 하는 파라미터 리스트
        list_parm_value = [] # 입력한 파라미터 값이 저장될 리스트
        for parm in parm_edit :
            if parm.default == Header.inspect._empty :
                name = parm.name
                list_parm_name.append(name)
                if (name != "self") :
                    list_parm_input.append(name)

        # 다이얼로그 비우기
        self.clearParameterDialog()
        if list_parm_input : # 입력할 파라미터가 있는 경우
            # 다이얼로그로 파라미터를 입력받아 파라미터 리스트 제작
            for parm in list_parm_input : # 입력할 파라미터 추가
                self.appendParameterDialog(parm)

            # 다이얼로그에 확인 버튼 추가 후 실행
            self.appendParameterDialogButton()
            self.dialog_parameter.exec_()

            if self.need_to_set_parameter : # 확인 버튼이 입력된 경우
                for parm in list_parm_name : # 파라미터 정보를 변환
                    if parm == "self" :
                        pass
                    else :
                        value = self.dict_parm_dialog[parm].text()
                        if not value : value = 0
                        list_parm_value.append(value)

                self.need_to_set_parameter = False
                # 입력된 파라미터에 따라 위젯 데이터 수정
                try :
                    frame.widget.editData(*list_parm_value)
                except :
                    self.showErrorDialog(3)
                    return
        else : # 파라미터가 self 뿐인 경우
            try :
                frame.widget.editData()
            except :
                self.showErrorDialog(3)
                return

    def setInitialLocation(self) :
        x = Header.random.randint(10, 60)
        y = Header.random.randint(10, 70)
        return x, y

    # 드래그 드롭 관련 함수
    def dragEnterEvent(self, e : Header.QDragEnterEvent) :
        e.accept()

    def dropEvent(self, e : Header.QDropEvent) :
        position = e.pos()
        try :
            mime_str = "move widget"
            offset = e.mimeData().data(mime_str)
            order = offset.data().decode('utf-8')
            for frame in self.list_frame :
                if frame.order == int(order) :
                    frame.move(position - Header.QPoint(15, 15))

            e.setDropAction(Header.Qt.MoveAction)
            e.accept()
        except : 
            print("Error in drop event")


    def closeWidget(self, order) :
        print("do closeWidget at Programming :", order)


# 위젯의 이름과 버튼을 표시할 프레임 클래스
class WidgetFrame(Header.QWidget) :
    signal_edit_widget = Header.pyqtSignal(int)
    signal_close_widget = Header.pyqtSignal(int)

    def __init__(self, size_x, size_y, order, font, icon_move, icon_edit, icon_close) :
        super().__init__()
        self.size_x = size_x
        self.size_y = size_y
        self.order = order
        self.func_edit = None
        self.widget = None
        self.bg = Header.QWidget(self)

        self.setAcceptDrops(True)

        self.setFixedSize(self.size_x + 10, self.size_y + 30)
        self.bg.setFixedSize(self.size_x + 10, self.size_y + 30)
        #self.setStyleSheet("background-color : gray;")
        self.bg.setStyleSheet("background-color : #FFFFFFFF;")

        self.label_name = Header.QLabel("", self.bg)
        self.label_name.setFont(font)
        self.label_name.move(35, 5)

        self.button_move = DragPushButton("", self.order, self.bg)
        self.button_move.setIcon(icon_move)
        self.button_move.setIconSize(Header.QSize(20, 20))
        self.button_move.move(5, 5)

        self.button_edit = Header.QPushButton("", self.bg)
        self.button_edit.setIcon(icon_edit)
        self.button_edit.setIconSize(Header.QSize(20, 20))
        self.button_edit.move(self.size_x - 55, 5)
        self.button_edit.clicked.connect(self.editWidgetData)

        self.button_close = Header.QPushButton("", self.bg)
        self.button_close.setIcon(icon_close)
        self.button_close.setIconSize(Header.QSize(20, 20))
        self.button_close.move(self.size_x - 25, 5)
        self.button_close.clicked.connect(self.closeWidget)

    def setName(self, name) :
        self.label_name.setText(name)
        self.label_name.adjustSize()

    def setWidget(self, widget) :
        self.widget = widget
        widget.setParent(self.bg)
        self.setName(widget.getName())

    def getWidget(self) : return self.widget

    def setSize(self, x, y) :
        self.size_x = x
        self.size_y = y
        self.setFixedSize(self.size_x + 10, self.size_y + 30)
        self.bg.setFixedSize(self.size_x + 10, self.size_y + 30)
        self.button_edit.move(self.size_x - 55, 5)
        self.button_close.move(self.size_x - 25, 5)

    def setEditFunction(self, func) : self.func_edit = func

    def getEditFunction(self) : return self.func_edit

    def editWidgetData(self) :
        #print("emit signal edit :", self.label_name.text(), self.signal_edit_widget)
        # 위젯의 일부 데이터 수정
        self.signal_edit_widget.emit(self.order)
        # 데이터가 변경된 후 프레임 또한 변경
        self.setName(self.widget.getName())
        (x, y) = self.widget.getSize()
        self.setSize(x, y)

    def closeWidget(self) :
        print("do closeWidget at Frame")
        self.signal_close_widget.emit(self.order)


# 드래그, 드롭이 가능한 pushbutton 클래스 제작
class DragPushButton(Header.QPushButton) :
    def __init__(self, title, order, parent) :
        #super().__init__(self, title, parent)
        Header.QPushButton.__init__(self, title, parent)
        self.p = parent
        self.order = order
        self.offset = 0

    def mouseMoveEvent(self, e : Header.QMouseEvent) :
        # 오른쪽 클릭만 입력 허용
        if e.buttons() != Header.Qt.LeftButton :
            return

        # 데이터 전송을 위한 Mime 객체 선언
        # 데이터 타입, 전송할 데이터를 bytes 형으로 저장함
        mime_data = Header.QMimeData()
        mime_str = "move widget"
        mime_data.setData(mime_str, b"%d" %(self.order))

        drag = Header.QDrag(self)
        # Mime 데이터를 Drag에 설정
        drag.setMimeData(mime_data)
        # 드래그시 버튼의 모양을 유지하기 위해 QPixmap에 모양을 렌더링
        pixmap = Header.QPixmap(self.size())
        self.render(pixmap)
        drag.setPixmap(pixmap)

        drag.setHotSpot(e.pos() - self.rect().topLeft())
        drag.exec_(Header.Qt.MoveAction)
