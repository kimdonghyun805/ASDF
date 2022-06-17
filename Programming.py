import Header

class Programming(Header.QWidget) :
    signal_pass_data_to_toolbar = Header.pyqtSignal(list)
    signal_request_widget = Header.pyqtSignal(str)

    def __init__(self, size_x, size_y, dictionary_icon, font, path_widgetfiles) :
        super().__init__()
        self.size_x = size_x
        self.size_y = size_y
        
        self.icon_move = dictionary_icon["move"]
        self.icon_edit = dictionary_icon["edit"]
        self.icon_close = dictionary_icon["close"]

        self.font = font
        self.path_widgetfiles = path_widgetfiles

        self.order = 0
        self.setAcceptDrops(True)

        self.resize(Header.QSize(self.size_x, self.size_y))
        self.setFixedSize(self.size_x, self.size_y)

        self.widget = Header.QWidget(self)
        self.widget.resize(Header.QSize(self.size_x - 20, self.size_y - 20))
        self.setFixedSize(self.size_x - 20, self.size_y - 20)
        self.widget.move(0, 0)

        #self.widget.setStyleSheet("border-style : solid; border-width : 2px; border-color : #00FF00;") # 위젯 스타일 - 초록
        self.title = Header.QLabel("Program", self.widget)
        self.title.setFont(self.font)
        self.title.move(0, 0)

        # 다이얼로그 사용을 위한 변수
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
        self.temp_widgetfile = {}

    # 에러 발생시 원인을 표시하는 다이얼로그
    def makeErrorDialog(self) :
        dialog = Header.QDialog(self.widget, Header.Qt.WindowTitleHint | Header.Qt.WindowCloseButtonHint)
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
        # 5 : 위젯의 연결에 필요한 함수 connectWidget이 작성되어있지 않거나, 오류가 있음
        # 6 : 연결시 지정한 위젯이 존재하지 않음
        # 7 : 위젯 삭제 불가능
        # 8 : 전달받은 위젯 데이터로 위젯을 생성할 수 없음
        message = ""
        if (error_no == 1) :
            message = "위젯 파일에 오류가 있거나\n잘못된 데이터가 입력되었습니다."
        elif (error_no == 2) :
            message = "더 이상 위젯을 생성할 수 없습니다."
        elif (error_no == 3) :
            message = "위젯의 데이터 수정기능에\n오류가 있거나 잘못된 데이터가\n입력되었습니다."
        elif (error_no == 4) :
            message = "위젯의 특정 데이터가\n손실되어 있습니다."
        elif (error_no == 5) :
            message = "위젯의 연결에 필요한 기능에\n문제가 있습니다."
        elif (error_no == 6) :
            message = "지정한 위젯이 존재하지 않습니다."
        elif (error_no == 7) :
            message = "위젯을 삭제할 수 없습니다."
        elif (error_no == 8) :
            message = "저장 파일 또는 위젯\n파일이 변경되어 파일을\n불러올 수 없습니다."
        else :
            message = "알수 없는 오류가 발생했습니다."

        label = self.dialog_error.findChild(Header.QLabel)
        label.setText(message)
        self.dialog_error.exec_()


    def makeParameterDialog(self) :
        dialog = Header.QDialog(None, Header.Qt.WindowTitleHint | Header.Qt.WindowCloseButtonHint)
        dialog.setWindowTitle("위젯 정보 입력")
        dialog.setFixedWidth(self.size_x_dialog_default)
        dialog.setFixedHeight(self.size_y_dialog_default)

        return dialog

    # 다이얼로그에 입력값 생성
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

    # 다이얼로그에 확인, 취소 버튼 추가
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

    # 다이얼로그 초기화
    def clearParameterDialog(self) : 
        del(self.dialog_parameter)
        self.dialog_parameter = self.makeParameterDialog()
        self.size_x_dialog = self.size_x_dialog_default
        self.size_y_dialog = self.size_y_dialog_default
        del(self.dict_parm_dialog)
        self.dict_parm_dialog = {}
        self.need_to_set_parameter = False

    def clickedDialogOk(self, t_or_f) :
        self.need_to_set_parameter = t_or_f
        self.dialog_parameter.close()

    # 위젯 객체 생성 준비
    def checkParameters(self, data_widgetfiles) :
        # widget list 에서 위젯 생성 버튼 입력시 실행
        # 위젯 파일의 정보를 받아 위젯 객체 생성에 필요한 정보 추출
        if self.num_widget >= 10 :
            self.showErrorDialog(2) # 위젯은 10개 초과로 생성될 수 없음
            return

        # 위젯의 클래스 정보 - 객체 생성을 위함
        class_widget = data_widgetfiles["class"]

        # 위젯 생성에 필요한 함수 추출
        func_init = data_widgetfiles["function"]["__init__"]
        func_edit_data = data_widgetfiles["function"]["editData"]
        func_set_connection = None
        func_get_connection = None
        if data_widgetfiles["connecting"] : # 연결이 필요한 위젯인 경우, 연결에 필요한 함수 추출
            func_set_connection = data_widgetfiles["function"]["setConnection"]
            func_get_connection = data_widgetfiles["function"]["getConnection"]

        # 생성자의 파라미터 확인
        parm_init = Header.inspect.signature(func_init).parameters.values()

        # 입력받아야 하는 파라미터 추출
        list_parm_name = [] # 설정해야 하는 모든 파라미터 리스트
        list_parm_input = [] # 입력해야 하는 파라미터 리스트
        list_parm_value = [] # 입력한 파라미터 값이 저장될 리스트
        for parm in parm_init :
            if parm.default == Header.inspect._empty : # 초기화 값이 없으며
                name = parm.name
                list_parm_name.append(name)
                if (name != "self") and (name != "order") : # self, order가 아닌 파라미터
                    list_parm_input.append(name) # 값을 입력받야야 하는 파라미터 추출

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
                # 입력된 파라미터에 따라 위젯 생성
                self.createWidget(class_widget, list_parm_value, func_edit_data, func_set_connection, func_get_connection)

        else : # 파라미터가 self 혹은 self, order 뿐인 경우 -> 입력할 파라미터가 없는 경우
            if "order" in list_parm_name :
                self.order = self.order + 1
                list_parm_value.append(self.order)
            # 위젯 생성
            self.createWidget(class_widget, list_parm_value, func_edit_data, func_set_connection, func_get_connection)
 
    # 위젯의 객체를 생성
    def createWidget(self, class_widget, list_parm, func_edit, func_set_connection, func_get_connection) :
        object_widget = None
        try :
            if list_parm : # 입력받은 파라미터에 맞춰 위젯 객체 생성
                object_widget = class_widget(*list_parm)
            else :
                object_widget = class_widget()
            if object_widget.getOrder() == 0 : # 생성시 order가 지정되지 않은 경우
                self.order = self.order + 1 # order값을 지정
                object_widget.setOrder(self.order)
        except :
            # 잘못된 파라미터 값이 지정된 경우, 오류 발생
            self.showErrorDialog(1)
            return

        # 연결 대상이 필요한 경우를 확인하고 지정함
        try :
            if object_widget.is_connecting :
                # 위젯이 연결 기능이 있으나 set_connection, get_connection 중 하나라도 작성되어 있지 않은 경우
                if (not func_set_connection) or (not func_get_connection) : 
                    self.showErrorDialog(5)
                    return

                # 연결 함수 setConnection
                parm_init = Header.inspect.signature(func_set_connection).parameters.values()

                # 입력받아야 하는 파라미터 추출
                list_parm_name = [] # 설정해야 하는 모든 파라미터 리스트
                list_parm_input = [] # 입력해야 하는 파라미터 리스트
                list_parm_value = [] # 입력한 파라미터 값(위젯 이름)이 저장될 리스트
                list_parm_widget = [] # 입력한 위젯 이름에 대한 위젯 객체가 저장될 리스트
                for parm in parm_init :
                    if parm.default == Header.inspect._empty :
                        name = parm.name
                        list_parm_name.append(name)
                        if name != "self" :
                            list_parm_input.append(name)

                # 파라미터에 연결될 위젯의 이름을 입력받음
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
                        #self.need_to_set_parameter = False

                        # 입력된 파라미터에 따라 위젯 연결
                        # 입력받은 값은 위젯의 이름(name)
                        # 파라미터 명칭으로 지목된 kind의 위젯을 확인, 입력값과 이름이 같은 경우 연결 대상이 됨
                        for n in range(0, len(list_parm_input)) :
                            list_widget_kind = self.getWidgetListAsKind(str(list_parm_input[n]))
                            is_found = False
                            if not list_widget_kind :
                                self.showErrorDialog(6)
                                return
                            for w in list_widget_kind :
                                if w.getName() == str(list_parm_value[n]) :
                                    list_parm_widget.append(w)
                                    is_found = True
                                    break
                            if not is_found :
                                self.showErrorDialog(6)
                                return
                        if len(list_parm_value) != len(list_parm_widget) :
                            self.showErrorDialog(6)
                            return

                        # 모든 파라미터에 대해 연결할 위젯을 탐색한 경우
                        # 위젯의 함수 setConnection 수행
                        try :
                            func_set_connection(object_widget, *list_parm_widget)
                        except :
                            self.showErrorDialog(5)
                            return
                        for w in list_parm_widget :
                            w.is_connected = True
                    else : # 연결이 취소된 경우
                        return
                else : # 입력할 파라미터(list_parm_value)가 없는 경우
                    func_set_connection(object_widget)
        except :
            #위젯에 is_connecting, is_connected 변수가 없는 경우
            self.showErrorDialog(4)
            return

        # 생성된 위젯을 인터페이스에 표시
        self.list_widget.append(object_widget)
        self.num_widget = self.num_widget + 1

        # 위젯과 버튼을 표시할 프레임 제작
        frame = self.makeWidgetFrame(object_widget, func_edit, func_get_connection)
        self.list_frame.append(frame)
        
        loc_x, loc_y = self.setInitialLocation()
        frame.move(loc_x, loc_y)
        frame.show()

    def getWidgetListAsKind(self, kind) : # 생성된 위젯 중에서 kind가 일치하는 것을 탐색 
        list_widget_kind = []
        for widget in self.list_widget :
            if widget.getKind() == kind :
                list_widget_kind.append(widget)
        return list_widget_kind

    # 위젯을 표시하고 일부 기능을 가지는 프레임 생성
    def makeWidgetFrame(self, object, func_edit, func_get_connection) :
        (x, y) = object.getSize()
        if x == 0 : x = 100 # 크기가 0인 경우 프레임은 표시되도록 값을 조정
        if y == 0 : y = 50
        order = object.getOrder()
        frame = WidgetFrame(x, y, order, self.font, self.icon_move, self.icon_edit, self.icon_close)
        frame.setParent(self.widget)
        frame.setWidget(object)
        frame.setEditFunction(func_edit)
        frame.setGetConnectionFunction(func_get_connection)
        frame.signal_edit_widget.connect(self.editWidgetData)
        frame.signal_close_widget.connect(self.closeWidget)
        object.move(5, 30)

        return frame

    def editWidgetData(self, order) :
        # 위젯의 일부 데이터 수정 - 위젯의 editData 호출
        frame = None
        for f in self.list_frame :
            if f.order == order : # order로 위젯 탐색
                frame = f
        if not frame :
            print("Widget could not be found through order")
            return
        parm_edit = Header.inspect.signature(frame.func_edit).parameters.values()
        # 입력받아야 하는 파라미터 추출
        list_parm_name = [] # 설정해야 하는 모든 파라미터 리스트
        list_parm_input = [] # 입력해야 하는 파라미터 리스트
        list_parm_value = [] # 입력한 파라미터 값이 저장될 리스트
        for parm in parm_edit :
            if parm.default == Header.inspect._empty : # 초기화 값이 없으며
                name = parm.name
                list_parm_name.append(name)
                if (name != "self") : # self가 아닌 파라미터
                    list_parm_input.append(name) # 값을 입력받아야 하는 파라미터 추출

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

                # 입력된 파라미터에 따라 위젯 데이터 수정
                try :
                    frame.func_edit(frame.widget, *list_parm_value)
                except :
                    self.showErrorDialog(3) # 파라미터에 잘못된 값을 입력
                    return
        else : # 파라미터가 self 뿐인 경우
            try :
                #frame.widget.editData()
                frame.func_edit(frame.widget)
            except :
                self.showErrorDialog(3)
                return

    # 위젯의 초기 생성 위치를 난수로 생성
    def setInitialLocation(self) :
        x = Header.random.randint(10, 60)
        y = Header.random.randint(10, 70)
        return x, y

    # 위치 이동에 사용되는드래그 드롭 관련 함수
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

    # 위젯 삭제 조건 확인 후 삭제
    def closeWidget(self, order) :
        frame = None
        for f in self.list_frame :
            if f.order == order : # order로 프레임 탐색
                frame = f
        if not frame :
            print("Widget could not be found through order")
            return
        widget = frame.getWidget()

        # 위젯이 연결중인 경우 삭제 불가능
        try :
            if widget.is_connected :
                self.showErrorDialog(7)
                return
        except :
            self.showErrorDialog(4)
            return

        # 연결 대상이 아닌 경우 삭제 가능
        self.deleteWidget(widget, frame)

    # 위젯을 삭제
    def deleteWidget(self, widget, frame) :
        # 연결중인 위젯들이 있는 경우, 각 위젯의 is_connected = false 변경
        try :
            if widget.is_connecting :
                list_connected_widget = frame.func_get_connection(widget)
                for w in list_connected_widget :
                    w.is_connected = False
        except :
            self.showErrorDialog(4)
            return
        # 인터페이스 상에서 삭제
        frame.setParent(None)
        # 리스트 상에서 삭제
        self.list_widget.remove(widget)
        self.list_frame.remove(frame)
        self.num_widget = self.num_widget - 1
        # 객체 삭제
        del widget
        del frame

    def makeAllWidgetData(self) :
        self.list_data_widget = [] # 모든 위젯 데이터를 저장할 변수
        for n in range(0, len(self.list_widget)) :
            # 각 위젯에 대한 getData() 정보와 위치 정보를 가져와야 함
            data_widget = self.list_widget[n].getData()
            loc_frame = self.list_frame[n].pos()
            data_widget["location_x"] = loc_frame.x()
            data_widget["location_y"] = loc_frame.y()
            self.list_data_widget.append(data_widget)

        # toolbar에 데이터를 넘겨줌
        self.signal_pass_data_to_toolbar.emit(self.list_data_widget)

    def setWidgetFile(self, data_widgetfile) :
        self.temp_widgetfile = data_widgetfile

    def makeWidgetFromData(self, list_data_widget) :
        # 현재 생성중인 위젯 모두 삭제
        for n in range(len(self.list_widget)-1, -1, -1) : # 이후에 생성된 위젯부터 삭제
            d_widget = self.list_widget[n]
            d_frame = self.list_frame[n]
            # 인터페이스 상에서 삭제
            d_frame.setParent(None)
            # 리스트 상에서 삭제
            self.list_widget.remove(d_widget)
            self.list_frame.remove(d_frame)
            self.num_widget = self.num_widget - 1
            # 객체 삭제
            del d_widget
            del d_frame
        
        # 각 데이터에 대해 위젯 생성
        for data_widget in list_data_widget :
            widget_name = data_widget["kind"]
            path_widget = self.path_widgetfiles + "\\" + widget_name + ".py"
            
            self.temp_widgetfile = {}
            self.signal_request_widget.emit(widget_name)
            if not self.temp_widgetfile : # 위젯 파일 데이터를 찾을 수 없는 경우
                self.showErrorDialog(8)
                return
            
            # 위젯의 클래스 정보 - 객체 생성을 위함
            class_widget = self.temp_widgetfile["class"]

            # 위젯 생성에 필요한 함수 추출
            func_init = self.temp_widgetfile["function"]["__init__"]
            func_edit_data = self.temp_widgetfile["function"]["editData"]
            # 위젯 객체 생성 - 생성자의 파라미터 확인
            parm_init = Header.inspect.signature(func_init).parameters.values()
            
            list_parm_name = [] # 설정해야 하는 모든 파라미터 리스트
            list_parm_input = [] # 입력해야 하는 파라미터 리스트
            list_parm_value = [] # 입력한 파라미터 값이 저장될 리스트
            for parm in parm_init :
                if parm.default == Header.inspect._empty : # 초기화 값이 없으며
                    name = parm.name
                    list_parm_name.append(name)
                    if (name != "self") and (name != "order") : # self, order가 아닌 파라미터
                        list_parm_input.append(name) # 값을 입력받야야 하는 파라미터 추출
                        list_parm_value.append(0) # 모든 파라미터 0으로 설정
            
            # 모든 파라미터를 0으로하여 위젯 생성
            object_widget = None
            try :
                if list_parm_value : # 입력받은 파라미터에 맞춰 위젯 객체 생성
                    object_widget = class_widget(*list_parm_value)
                else :
                    object_widget = class_widget()
                if object_widget.getOrder() == 0 : # order 값 설정
                    object_widget.setOrder(data_widget["order"])
                    if self.order < data_widget["order"] :
                        self.order = data_widget["order"]

                # 연결이 필요한 경우
                func_set_connection = None
                func_get_connection = None
                if self.temp_widgetfile["connecting"] : # 위젯이 연결이 필요하면서
                    if "connection" in data_widget : # 연결 대상이 존재하는 경우
                        func_set_connection = self.temp_widgetfile["function"]["setConnection"]
                        func_get_connection = self.temp_widgetfile["function"]["getConnection"]
                        
                        # 연결 함수 setConnection
                        parm_init = Header.inspect.signature(func_set_connection).parameters.values()

                        # 입력받아야 하는 파라미터 추출
                        list_parm_name = [] # 설정해야 하는 모든 파라미터 리스트
                        list_parm_input = [] # 입력해야 하는 파라미터 리스트
                        list_parm_widget = [] # 파라미터에 대한 위젯 객체가 저장될 리스트
                        for parm in parm_init :
                            if parm.default == Header.inspect._empty :
                                name = parm.name
                                list_parm_name.append(name)
                                if name != "self" :
                                    list_parm_input.append(name)
                        
                        # list_parm_input의 각 요소와 data_widget["connection"]의 ["kind"]이 일치
                        for kind in list_parm_input :
                            name = ""
                            is_found = False
                            for d in data_widget["connection"] :
                                if d["kind"] == kind :
                                    name = d["name"]
                            # kind와 name이 일치하는 위젯을 찾아 list_parm_widget에 추가
                            list_widget_kind = self.getWidgetListAsKind(kind)
                            if not list_widget_kind :
                                self.showErrorDialog(8)
                                return
                            for widget in list_widget_kind :
                                if widget.getName() == name :
                                    list_parm_widget.append(widget)
                                    is_found = True
                                    break
                            if not is_found :
                                self.showErrorDialog(8)
                                return

                        if len(list_parm_input) != len(list_parm_widget) : # 연결에 필요한 위젯을 모두 찾지 못한 경우
                            print(len(list_parm_input), len(list_parm_widget))
                            self.showErrorDialog(8)
                            return

                        # 연결 실행
                        object_widget.setConnection(*list_parm_widget)

                # setData 호출하에 위젯 데이터 설정
                object_widget.setData(data_widget)    
                # 만들어진 위젯에 대한 프레임 생성
                frame = self.makeWidgetFrame(object_widget, func_edit_data, func_get_connection)
                # 위젯과 프레임을 리스트에 추가
                self.list_widget.append(object_widget)
                self.list_frame.append(frame)
                self.num_widget = self.num_widget + 1
                # 프레임을 이동하고 인터페이스에 표시
                frame.move(data_widget["location_x"], data_widget["location_y"])
                frame.show()
            except :
                self.showErrorDialog(8)
                return


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
        self.func_get_connection = None
        self.widget = None
        self.bg = Header.QWidget(self)

        self.setAcceptDrops(True)

        self.setFixedSize(self.size_x + 10, self.size_y + 35)
        self.bg.setFixedSize(self.size_x + 10, self.size_y + 35)
        self.bg.setStyleSheet("background-color : #FFDDDDDD;")

        self.label_name = Header.QLabel("", self.bg)
        self.label_name.setFont(font)
        self.label_name.move(40, 5)

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
        self.setFixedSize(self.size_x + 10, self.size_y + 35)
        self.bg.setFixedSize(self.size_x + 10, self.size_y + 35)
        self.button_edit.move(self.size_x - 55, 5)
        self.button_close.move(self.size_x - 25, 5)

    def setEditFunction(self, func) : self.func_edit = func

    def getEditFunction(self) : return self.func_edit

    def setGetConnectionFunction(self, func) : self.func_get_connection = func

    def getGetConnectionFunction(self) : return self.func_get_connection

    def editWidgetData(self) :
        # 위젯의 일부 데이터 수정
        self.signal_edit_widget.emit(self.order)
        # 데이터가 변경된 후 프레임 또한 변경
        self.setName(self.widget.getName())
        (x, y) = self.widget.getSize()
        self.setSize(x, y)

    def closeWidget(self) :
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
