import Header

class WidgetList (Header.QScrollArea) :
    signal_add = Header.pyqtSignal(dict)
    signal_pass_widgetfile = Header.pyqtSignal(dict)

    def __init__(self, size_x, size_y, dictionary_icon, font, path_widgetfiles) :
        super().__init__()
        self.size_x = size_x
        self.size_y = size_y

        self.icon_info = dictionary_icon["info"]
        self.icon_edit = dictionary_icon["edit"]
        self.icon_add = dictionary_icon["add"]

        self.font = font
        self.path_widgetfiles = path_widgetfiles

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

        #self.setStyleSheet("border-style : solid; border-width : 2px; border-color : #FF0000;") # 위젯 스타일 - 빨강
        self.setVisible(True)

        #(self.dialog, self.info_dialog) = self.makeInfoDialog()
        self.dialog = self.makeInfoDialog()

        self.list_widgetfiles = self.checkWidgetFile()
        self.displayWidgetFileList(self.list_widgetfiles)


    def setWidgetHeight(self, up_or_down, height) :
        if up_or_down :
            # true인 경우 up - 높이 증가
            self.now_height_widget = self.now_height_widget + height + 10
        else :
            # false인 경우 down - 높이 감소
            if now_height_widget >= 0 :
                self.now_height_widget = self.now_height_widget - height - 10
                if self.now_height_widget < 0 : 
                    self.now_height_widget = 0
        self.widget.setFixedHeight(self.now_height_widget)

    # 위젯 파일을 인터페이스에 표시
    def makeWidgetFile(self, data_widgetfile) :
        name = data_widgetfile["name"]
        path = data_widgetfile["path"]
        func_info = data_widgetfile["function"]["getInfo"]

        widget_file = Header.QGroupBox()
        width = 200
        height = 110
        widget_file.resize(Header.QSize(width, height))
        widget_file.setFixedSize(width, height)
        widget_file.setStyleSheet("background-color : #FFDDDDDD;")

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
        button_info.clicked.connect(lambda : self.displayWidgetInfo(name, func_info))

        button_edit = Header.QPushButton(None, widget_file)
        button_edit.setIcon(self.icon_edit)
        button_edit.setIconSize(Header.QSize(35, 35))
        button_edit.move(80, 60)
        button_edit.setToolTip("이 위젯 파일의 내용을 수정합니다.")
        button_edit.clicked.connect(lambda : self.editWidgetFile(path))

        button_add = Header.QPushButton(None, widget_file)
        button_add.setIcon(self.icon_add)
        button_add.setIconSize(Header.QSize(35, 35))
        button_add.move(140, 60)
        button_add.setToolTip("이 위젯을 사용하기 위해 생성합니다.")
        button_add.clicked.connect(lambda : self.makeWidget(data_widgetfile))

        #widget_file.setStyleSheet("border-style : solid; border-width : 2px; border-color : #000000;") # 위젯 스타일 - 검정
        return widget_file
        
    def makeInfoDialog (self) :
        dialog = Header.QDialog(None, Header.Qt.WindowTitleHint | Header.Qt.WindowCloseButtonHint)
        dialog.setWindowTitle("info")
        dialog.setFixedSize(300, 200)

        text_info = Header.QTextEdit("widget information", dialog)
        text_info.resize(280, 180)
        text_info.move(10, 10)
        text_info.setFont(self.font)
        text_info.setAcceptRichText(False)
        text_info.setReadOnly(True)

        return dialog

    def displayWidgetInfo(self, name, func_info) :
        info = func_info(None)
        self.dialog.setWindowTitle(name + " 위젯 정보")
        textedit = self.dialog.findChild(Header.QTextEdit)
        textedit.setText(info)
        self.dialog.exec_()

    def editWidgetFile(self, path) :
        Header.os.popen(path)

    def makeWidget(self, data_widgetfile) :
        # data_widgetfile = { name, path, class, function } 형태로 구성
        self.signal_add.emit(data_widgetfile)


    def checkWidgetFile(self) :
        # 폴더 위치에서 위젯 파일들을 확인
        list_python_files = [] # .py 파일 리스트
        list_widget_files = [] # 모듈 정보 리스트
        
        try :
            list_resources = Header.os.listdir(self.path_widgetfiles)
            list_python_files = list(f for f in list_resources if f.endswith(".py")) # .py 파일 전부 확인
        except :
            print("Directory access denied :", self.path_widgetfiles)
            Header.sys.exit(0)

        # 파이썬 파일 리스트에서 각 파일을 모듈로 임포트하여 (name, module)의 리스트인 list_widget_file 제작
        for file_py in list_python_files :
            t_name = file_py[:-3] # 파일 이름에서 .py 제거 -> 모듈 이름
            try :
                t_module = Header.importlib.import_module(t_name, self.path_widgetfiles)
                if t_name != "default" : # 기본 파일 default는 인식하지 않음
                    tuple_widget = (t_name, t_module)
                    list_widget_files.append(tuple_widget)
            except :
                # 위젯 파일을 import 할 수 없는 경우
                print("errors at widget file :", t_name)
                continue
        #print("list_widget_files :", list_widget_files)

        # 필수 함수 editData, getData, setData, getOrder, setOrder, getInfo, 
        #           getSize, getName, setName, getKind, deleteWidget
        list_mandatory_func = ["__init__", "editData", "getData", "setData", "getOrder", "setOrder",
                               "getInfo", "getSize", "getName", "setName", "getKind"]
        list_dict_widget_files = []
        for file_widget in list_widget_files :  # 각 모듈에 대해
            dict_widget_files = {}
            w_name = None
            w_path = None
            w_class = None
            w_connecting = False
            dict_w_func = {}
            
            list_class = Header.inspect.getmembers(file_widget[1], Header.inspect.isclass) # 클래스 목록을 확인하고

            for class_widget in reversed(list_class) : # 클래스 목록에서
                if class_widget[0] == file_widget[0] : # 클래스 이름과 모듈 이름이 같은 클래스가 있는 경우
                    w_name = file_widget[0]
                    w_path = file_widget[1].__file__
                    w_class = class_widget[1] # 정보를 저장
                    
                    is_get_c = False
                    is_set_c = False
                    # 모듈의 함수 리스트를 가져오고
                    list_func = Header.inspect.getmembers(w_class, Header.inspect.isfunction)
                    num_func = 0
                    for func in list_func :
                        for name in list_mandatory_func :
                            if func[0] == name : # 필수 함수가 작성되어 있는 경우, 정보를 저장
                                dict_w_func[name] = func[1]
                                num_func += 1
                            if func[0] == "setConnection" : # 연결에 필요한 함수들이 작성되어 있는 경우, 정보를 저장
                                dict_w_func["setConnection"] = func[1] # 필수 함수가 아니므로 확인을 위한 num_func 값을 조정하지 않음
                                is_set_c = True
                            elif func[0] == "getConnection" :
                                dict_w_func["getConnection"] = func[1]
                                is_get_c = True

                    if is_get_c and is_set_c :
                        w_connecting = True # 연결이 가능한지 아닌지 확인할 정보 설정

                    if num_func == len(list_mandatory_func) : # 모든 필수 함수가 작성되어 있는 경우, 딕셔너리에 데이터 저장
                        dict_widget_files["name"] = w_name
                        dict_widget_files["path"] = w_path
                        dict_widget_files["class"] = w_class
                        dict_widget_files["function"] = dict_w_func
                        dict_widget_files["connecting"] = w_connecting
                    else :
                        print("widget :", w_name, ", lost some mendatory functions :", len(list_mandatory_func) - num_func)
                    break # 이름이 같은 클래스를 찾은 경우 반복문 탈출

            # 조건을 모두 만족하여 데이터가 입력된 경우, 다른 모듈의 데이터와 연결하여 리스트 제작
            if dict_widget_files :
                list_dict_widget_files.append(dict_widget_files)

        return list_dict_widget_files

    def displayWidgetFileList(self, list_widgetfiles) :
        # 확인한 위젯 파일들의 목록을 인터페이스에 표시함
        # list_widgetfiles = [ { name, path, class, function, connecting }, ... ] 형태로 구성
        for widget_info in list_widgetfiles :
            widgetfile = self.makeWidgetFile(widget_info)
            self.layout.addWidget(widgetfile)
            self.setWidgetHeight(True, self.height_widget_file)

    # 특정 위젯 파일의 정보를 programming에 전달
    def getWidgetFile(self, name) :
        widgetfile = {}
        for data_widgetfile in self.list_widgetfiles :
            if data_widgetfile["name"] == name :
                widgetfile = data_widgetfile
        if not widgetfile :
            print("could not be found corresponding widget file :", name)
        self.signal_pass_widgetfile.emit(widgetfile)