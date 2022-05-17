import Header
from Toolbar import Toolbar
from WidgetList import WidgetList
from Programming import Programming

def checkDirectory(path) :
    if path_resources :
        if not Header.os.path.exists :
            print("Directory not found :", path)
            Header.sys.exit(0)
        else :
            print("Find Directory :", path)
    else :
        print("Path not founded :", path)
        Header.sys.exit(0)

def loadIcon(path_resources, name_icon, type_icon) :
    dictionary_icon = {}
    for name in name_icon :
        path_icon = path_resources + "\\" + name + type_icon
        icon = Header.QIcon(path_icon)
        dictionary_icon[name] = icon
    return dictionary_icon

def loadFont(path_resources, name_font, type_font) :
    path_font = path_resources + "\\" + name_font + type_font
    font_db = Header.QFontDatabase()
    font_db.addApplicationFont(path_font)
    #font = Header.QFont("Noto Sans KR Black") #폰트 명칭과 파일 명칭이 다름
    #font.setPointSize(10)
    #font.setPixelSize(20)
    font = "Noto Sans KR Black"
    return font

def checkResources(path_resources, type_icon, type_font) :
    checkDirectory(path_resources)
    try :
        list_resources = Header.os.listdir(path_resources)
    except :
        print("Directory access denied :", path_resources)
        Header.sys.exit(0)

    name_icon = ["add", "close", "edit", "info", "load", "move", "new", "save"]
    name_font = "NotoSansKR-Black"
    #name_font = "Koulen-Regular"

    lost_icon = []
    for name in name_icon :
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

def makeToolbar(dictionary_icon, font, path_savefile) :
    # 툴바 인터페이스 객체를 만들어 리턴
    f = Header.QFont(font) #폰트 명칭과 파일 명칭이 다름
    f.setPointSize(10)
    f.setPixelSize(30)
    f.setBold(True)
    toolbar = Toolbar(dictionary_icon, f, path_savefile)
    return toolbar

def makeWidgetList(size_x, size_y, dictionary_icon, font, widget) :
    # 위젯리스트 인터페이스 객체를 만들 리턴
    f = Header.QFont(font) #폰트 명칭과 파일 명칭이 다름
    f.setPointSize(10)
    f.setPixelSize(20)
    widget_list = WidgetList(size_x, size_y, dictionary_icon, f, widget)
    return widget_list

def makeProgramming(size_x, size_y, dictionary_icon, font, widget) :
    # 프로그래밍 인터페이스 객체를 만들어 리턴
    f = Header.QFont(font) #폰트 명칭과 파일 명칭이 다름
    f.setPointSize(10)
    f.setPixelSize(15)
    f.setItalic(True)
    programming = Programming(size_x, size_y, dictionary_icon, f, widget)
    return programming

class MainWindow (Header.QMainWindow) :
    def __init__(self, size_x, size_y, title) :
        super().__init__(None, Header.Qt.WindowTitleHint
                         | Header.Qt.WindowMinimizeButtonHint
                         | Header.Qt.WindowCloseButtonHint)
        self.size_x = size_x
        self.size_y = size_y
        self.title = title
        #self.font = Header.QFont(font) #검증필요

        self.setWindowTitle(self.title)
        self.resize(Header.QSize(self.size_x, self.size_y))
        self.setFixedWidth(self.size_x)
        self.setFixedHeight(self.size_y)

        self.widget = Header.QWidget()
        #self.widget.resize(self.size_x, self.size_y - 100)
        #self.widget.setFixedWidth(self.size_x)
        #self.widget.setFixedHeight(self.size_y - 50)
        self.setCentralWidget(self.widget)

        self.layout = Header.QHBoxLayout()
        self.widget.setLayout(self.layout)

        self.widget.setStyleSheet("border-style : solid; border-width : 2px; border-color : #0000FF;")


if __name__ == "__main__" :
    path_resources = "Resources"
    path_savefile = "SaveFiles"
    title = "ASDF"

    size_x_main = 1280
    size_y_main = 720

    size_x_widget_list = 240
    size_y_widget_list = 650

    size_x_programming = 1035
    size_y_programming = 670

    type_icon = ".png"
    type_font = ".otf"

    window = Header.QApplication(Header.sys.argv)
    (dictionary_icon, font) = checkResources(path_resources, type_icon, type_font)

    main = MainWindow(size_x_main, size_y_main, title)

    toolbar = makeToolbar(dictionary_icon, font, path_savefile)
    main.addToolBar(toolbar)

    widget_list = makeWidgetList(size_x_widget_list, size_y_widget_list, dictionary_icon, font, main.widget)
    main.layout.addWidget(widget_list)

    programming = makeProgramming(size_x_programming, size_y_programming, dictionary_icon, font, main.widget)
    main.layout.addWidget(programming)

    print("start")
    print("toolbar font :", toolbar.font.toString())
    print("widget_list font :", widget_list.font.toString())
    print("programming font :", programming.font.toString())
    main.show()
    
    Header.sys.exit(window.exec_())
