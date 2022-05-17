import Header

class Toolbar (Header.QToolBar) :
    def __init__(self, dictionary_icon, font, path_savefile) :
        super().__init__()
        self.path_savefile = path_savefile
        self.icon_new = dictionary_icon["new"]
        self.icon_save = dictionary_icon["save"]
        self.icon_load = dictionary_icon["load"]
        self.font = font
        #self.font.setBold(True)
        #self.font.setPixelSize(30)
        print("toolbar font :", self.font.toString())
        

        self.color_black = "Color : black"
        icon_size = 40
        self.setIconSize(Header.QSize(icon_size, icon_size))
        self.setMovable(False)

        self.addSeparator()
        label_widgets = Header.QLabel("위젯Widgets")
        label_widgets.setFont(self.font)
        label_widgets.setFixedWidth(250)
        label_widgets.setAlignment(Header.Qt.AlignCenter)
        label_widgets.setStyleSheet(self.color_black)
        self.addWidget(label_widgets)
        self.addSeparator()

        self.addSeparator()
        action_new = Header.QAction(self.icon_new, "Make New Widget File", self)
        action_new.triggered.connect(lambda : self.makeNewWidgetFile())
        self.addAction(action_new)
        self.addSeparator()

        self.addSeparator()
        action_save = Header.QAction(self.icon_save, "Save Program", self)
        action_save.triggered.connect(lambda : self.saveProgram())
        self.addAction(action_save)
        self.addSeparator()

        self.addSeparator()
        action_load = Header.QAction(self.icon_load, "Load Program", self)
        action_load.triggered.connect(lambda : self.loadProgram())
        self.addAction(action_load)
        self.addSeparator()

    def makeNewWidgetFile(self) :
        print("Do makeNewWidgetFile")

    def saveProgram(self) :
        print("Do saveProgram")

    def loadProgram(self) :
        print("Do loadProgram")