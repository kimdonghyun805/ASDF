import Header

class WidgetList (Header.QScrollArea) :
    def __init__(self, size_x, size_y, dictionary_icon, font, path_widgetfiles) :
        super().__init__()
        self.size_x = size_x
        self.size_y = size_y

        self.icon_info = dictionary_icon["info"]
        self.icon_edit = dictionary_icon["edit"]
        self.icon_add = dictionary_icon["add"]

        self.font = font
        self.path_widgetfiles = path_widgetfiles
        #Header.sys.path.append(".\\" + self.path_widgetfiles)

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

        self.list_widgetfiles = self.checkWidgetFile()
        self.displayWidgetFileList(self.list_widgetfiles)

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
        list_python_files = []
        list_widget_files = []
        
        try :
            list_resources = Header.os.listdir(self.path_widgetfiles)
            list_python_files = list(f for f in list_resources if f.endswith(".py"))
        except :
            print("Directory access denied :", self.path_widgetfiles)
            Header.sys.exit(0)

        print(".py list :", list_python_files)

        package = Header.importlib.import_module(self.path_widgetfiles)
        #print(dir(package))
        #m1 = getattr(package, list_python_files[0])
        #print(Header.sys.path)

        #Header.importlib.invalidate_caches()
        for p in list_python_files :
            d = {}
            d["name"] = p[:-3]
            d["module"] = Header.importlib.import_module(d["name"], self.path_widgetfiles)
            #d["module"] = __import__(d["name"])
            list_widget_files.append(d)

        print("widget file list :", list_widget_files)
        #print("1. :", dir(list_widget_files[0]["module"]))
        #print("2. :", dir(list_widget_files[0].items))
        #print("3. :", dir(list_widget_files[0].get))
        #print("4. :", dir(list_widget_files[0].values))

        #cls = getattr(list_widget_files[0]["module"], list_widget_files[0]["name"])
        #print(type(cls), "\n\n", cls)
        list_inspect = Header.inspect.getmembers(list_widget_files[0]["module"], Header.inspect.isclass) # 모듈의 클래스 확인
        print("A", list_inspect)
        cls_ins = None
        for l in reversed(list_inspect) :
            if l[0] == list_widget_files[0]["name"] : cls_ins = l # 모듈의 클래스 리스트에서 필요한 클래스 추출
        print("B", cls_ins)
        print("C", cls_ins[1]) # 모듈(파일) 이름과 클래스 이름이 같아야 함

        func_inspect = Header.inspect.getmembers(cls_ins[1], Header.inspect.isfunction) # 클래스의 함수 추출
        print("D", func_inspect)

        init_ins = None
        fun_ins = None
        for k in func_inspect :
            if k[0] == "setWidgetData" : 
                fun_ins = k # 함수 명칭을 통해 특정 함수 추출
            elif k[0] == "__init__" :
                init_ins = k
        print("E", fun_ins)
        print("F", init_ins)

        obj = cls_ins[1]() # 객체 생성
        #obj = init_ins[1](obj) # 생성자 함수로는 객체 생성 불가능
        print(type(cls_ins[1])) # wrapper 타입
        print(type(obj)) # 객체 타입 - 객체 생성 가능함

        fun_ins[1](obj, 5, 5) # 함수 실행 - 파라미터는 아직 확인할 수 없음
        lis = obj.getWidgetData() # 일반적인 함수호출 가능, 리턴 가능
        print("lis", lis)

        fun_sig = Header.inspect.signature(fun_ins[1]) # 함수 파라미터 정보를 가져옴
        init_sig = Header.inspect.signature(init_ins[1])
        print("G", type(fun_sig), fun_sig)
        print("H", fun_sig.parameters.values(), len(fun_sig.parameters.values())) # 파라미터 목록과 개수
        
        list_parm = []
        list_parm_value = []
        for a in fun_sig.parameters.values() :
            print(type(a.name), a.name, type(a.default), a.default, type(a.kind), a.kind)
            if a.default == Header.inspect._empty :
                if str(a.name) != "self" : 
                    print("need to set parameter :", a.name)
                    list_parm.append(a.name)
        print("I", list_parm)
        list_parm_value.append(obj)
        for b in list_parm :
            list_parm_value.append(99)
        print("J", list_parm_value)
        parm = fun_sig.bind(*list_parm_value) # 리스트 언패킹으로 파라미터 전달
        #parm = fun_sig.bind(list_parm_value[0], list_parm_value[1], list_parm_value[2])
        #parm = fun_sig.bind(obj, 7, 7)
        fun_ins[1](*parm.args, **parm.kwargs) # 바인드 되어있는 파라미터 정보로 함수 호출
        parm = fun_sig.bind(obj, 55, 55)
        fun_ins[1](*parm.args, **parm.kwargs)
        
        #fun_arg = Header.inspect.getargspec(fun_ins[1]) # 함수 파라미터 정보
        #init_arg = Header.inspect.getargspec(init_ins[1])
        #print("I", fun_arg)
        #print("J", init_arg)

        # self.지역변수를 객체 생성 이전에 알 방법 없음
        #init_code = Header.inspect.getmembers(init_ins[1], Header.inspect.iscode)
        #print("K", init_code[0][1].co_varnames) # 함수의 지역변수 목록
        #cls_code = Header.inspect.getmembers(cls_ins[1], Header.inspect.iscode)
        #print("L", cls_code)

        return list_widget_files

    def displayWidgetFileList(self, list_widgetfiles) :
        # 확인한 위젯 파일들의 목록을 위젯 형태로 만들어 표시함
        print("do displayWidgetFileList")