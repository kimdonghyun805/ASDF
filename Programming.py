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

