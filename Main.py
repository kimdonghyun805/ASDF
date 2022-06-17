import Header
from Toolbar import Toolbar
from WidgetList import WidgetList
from Programming import Programming

def checkDirectory(path) :
    if path_resources :
        if not Header.os.path.exists : # 디렉토리 존재 확인
            print("Directory not found :", path)
            Header.sys.exit(0)
        else :
            print("Find Directory :", path)
    else :
        print("Path not founded :", path)
        Header.sys.exit(0)

def loadIcon(path_resources, name_icon, type_icon) :
    dictionary_icon = {}
    for name in name_icon : # 이름에 맞는 아이콘 로딩
        path_icon = path_resources + "\\" + name + type_icon
        icon = Header.QIcon(path_icon)
        dictionary_icon[name] = icon
    return dictionary_icon

def loadFont(path_resources, name_font, type_font) :
    path_font = path_resources + "\\" + name_font + type_font
    font_db = Header.QFontDatabase()
    font_db.addApplicationFont(path_font)
    font = "Noto Sans KR Black" # 폰트 파일명과 폰트 객체의 이름이 다름
    return font

def checkResources(path_resources, type_icon, type_font) :
    try :
        list_resources = Header.os.listdir(path_resources)
    except :
        print("Directory access denied :", path_resources)
        Header.sys.exit(0)

    name_icon = ["add", "close", "edit", "info", "load", "move", "new", "save"] # 아이콘 파일 명칭
    name_font = "NotoSansKR-Black" # 폰트 파일 명칭
    #name_font = "Koulen-Regular"

    lost_icon = []
    for name in name_icon : # 아이콘 명칭과 타입 연결
        name = name + type_icon
        if not name in list_resources :
            lost_icon.append(name)

    if lost_icon :
        print("Icon file lost :", lost_icon)
        Header.sys.exit(0)
    
    if not (name_font + type_font) in list_resources :
        print("Font file lost :", name_font)
        Header.sys.exit(0)

    dictionary_icon = loadIcon(path_resources, name_icon, type_icon)
    font = loadFont(path_resources, name_font, type_font)

    return (dictionary_icon, font)

def makeToolbar(dictionary_icon, font, path_savefile, path_widgetfile) :
    # 툴바 인터페이스 객체를 만들어 리턴
    tf = Header.QFont(font)
    tf.setPointSize(10)
    tf.setPixelSize(30)
    tf.setBold(True)
    ef = Header.QFont(font)
    ef.setPointSize(20)
    ef.setPixelSize(16)
    ef.setBold(False)
    toolbar = Toolbar(dictionary_icon, tf, ef, path_savefile, path_widgetfile)
    return toolbar

def makeWidgetList(size_x, size_y, dictionary_icon, font, path_widgetfiles) :
    # 위젯리스트 인터페이스 객체를 만들 리턴
    f = Header.QFont(font)
    f.setPointSize(10)
    f.setPixelSize(20)
    widget_list = WidgetList(size_x, size_y, dictionary_icon, f, path_widgetfiles)
    return widget_list

def makeProgramming(size_x, size_y, dictionary_icon, font, path_widgetfiles) :
    # 프로그래밍 인터페이스 객체를 만들어 리턴
    f = Header.QFont(font)
    f.setPointSize(20)
    f.setPixelSize(16)
    f.setBold(False)
    programming = Programming(size_x, size_y, dictionary_icon, f, path_widgetfiles)
    return programming

class MainWindow (Header.QMainWindow) :
    def __init__(self, size_x, size_y, title) :
        super().__init__(None, Header.Qt.WindowTitleHint
                         | Header.Qt.WindowMinimizeButtonHint
                         | Header.Qt.WindowCloseButtonHint)
        self.size_x = size_x
        self.size_y = size_y
        self.title = title

        self.setWindowTitle(self.title)
        self.resize(Header.QSize(self.size_x, self.size_y))
        self.setFixedWidth(self.size_x)
        self.setFixedHeight(self.size_y)

        self.widget = Header.QWidget()
        self.setCentralWidget(self.widget)

        self.layout = Header.QHBoxLayout()
        self.widget.setLayout(self.layout)

        #self.widget.setStyleSheet("border-style : solid; border-width : 2px; border-color : #0000FF;") # 위젯 스타일 - 파랑


if __name__ == "__main__" :
    path_resources = "Resources"
    path_savefiles = "SaveFiles"
    path_widgetfiles = "WidgetFiles"
    try :
        path_now = Header.os.getcwd() # 현재 작업 디렉토리의 경로
        # 현재 작업 디렉토리 아래의 위젯 파일 폴더의 경로를 모듈 탐색 경로에 추가
        Header.sys.path.append(path_now + "\\" + path_widgetfiles)
    except :
        print("current work directory access denied")
        Header.sys.exit(0)

    title = "ASDF" # 프로그램 제목

    # 각 인터페이스 크기를 고정값으로 설정
    size_x_main = 1280
    size_y_main = 720

    size_x_widget_list = 240
    size_y_widget_list = 650

    size_x_programming = 1035
    size_y_programming = 670

    type_icon = ".png" # 아이콘 파일 타입
    type_font = ".otf" # 폰트 파일 타입

    # 필요한 디렉토리 확인
    checkDirectory(path_resources)
    checkDirectory(path_savefiles)
    checkDirectory(path_widgetfiles)

    # 인터페이스 생성
    window = Header.QApplication(Header.sys.argv)
    (dictionary_icon, font) = checkResources(path_resources, type_icon, type_font)

    main = MainWindow(size_x_main, size_y_main, title)

    toolbar = makeToolbar(dictionary_icon, font, path_savefiles, path_widgetfiles)
    main.addToolBar(toolbar)

    widget_list = makeWidgetList(size_x_widget_list, size_y_widget_list, dictionary_icon, font, path_widgetfiles)
    main.layout.addWidget(widget_list)

    programming = makeProgramming(size_x_programming, size_y_programming, dictionary_icon, font, path_widgetfiles)
    main.layout.addWidget(programming)

    widget_list.signal_add.connect(programming.checkParameters)
    toolbar.signal_request_data.connect(programming.makeAllWidgetData)
    programming.signal_pass_data_to_toolbar.connect(toolbar.saveData)
    toolbar.signal_pass_data_to_programming.connect(programming.makeWidgetFromData)
    programming.signal_request_widget.connect(widget_list.getWidgetFile)
    widget_list.signal_pass_widgetfile.connect(programming.setWidgetFile)

    main.show()
    
    Header.sys.exit(window.exec_())
