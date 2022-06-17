import Header

class Toolbar (Header.QToolBar) :
    signal_request_data = Header.pyqtSignal()
    signal_pass_data_to_programming = Header.pyqtSignal(list)

    def __init__(self, dictionary_icon, title_font, error_font, path_savefile, path_widgetfile) :
        super().__init__()
        self.path_savefile = path_savefile
        self.path_widgetfile = path_widgetfile
        self.icon_new = dictionary_icon["new"]
        self.icon_save = dictionary_icon["save"]
        self.icon_load = dictionary_icon["load"]
        self.title_font = title_font
        self.error_font = error_font

        icon_size = 40
        self.setIconSize(Header.QSize(icon_size, icon_size))
        self.setMovable(False)

        self.addSeparator()
        label_widgets = Header.QLabel("위젯 목록")
        label_widgets.setFont(self.title_font)
        label_widgets.setFixedWidth(240)
        label_widgets.setAlignment(Header.Qt.AlignCenter)
        self.addWidget(label_widgets)
        self.addSeparator()

        self.addSeparator()
        action_new = Header.QAction(self.icon_new, "새로운 위젯 파일을 생성합니다.", self)
        action_new.triggered.connect(lambda : self.makeNewWidgetFile())
        self.addAction(action_new)
        self.addSeparator()

        self.addSeparator()
        action_save = Header.QAction(self.icon_save, "현재 프로그램을 저장합니다.", self)
        action_save.triggered.connect(lambda : self.saveProgram())
        self.addAction(action_save)
        self.addSeparator()

        self.addSeparator()
        action_load = Header.QAction(self.icon_load, "저장된 프로그램을 불러옵니다.", self)
        action_load.triggered.connect(lambda : self.loadProgram())
        self.addAction(action_load)
        self.addSeparator()

        self.need_to_get_filename = False
        self.dialog_error = self.makeErrorDialog()
        self.dialog_file_select = self.makeFileSelectDialog()


    # 에러 발생시 원인을 표시하는 다이얼로그
    def makeErrorDialog(self) :
        dialog = Header.QDialog(self, Header.Qt.WindowTitleHint | Header.Qt.WindowCloseButtonHint)
        dialog.setWindowTitle("오류")
        dialog.setFixedSize(300, 120)

        label_message = Header.QLabel("", dialog)
        label_message.setFont(self.error_font)
        label_message.setFixedSize(260, 70)
        label_message.move(20, 10)

        button_close = Header.QPushButton("닫기", dialog)
        button_close.setFont(self.error_font)
        button_close.setFixedSize(100, 30)
        button_close.move(180, 80)
        button_close.clicked.connect(dialog.close)

        return dialog

    def showErrorDialog(self, error_no) :
        # error_no
        # 1 : 위젯 파일 디렉토리에 접근 불가능, 혹은 default.py 없음
        # 2 : 위젯 파일 생성 시 이미 존재하는 이름 지정
        # 3 : 위젯 파일 생성 시 기본 위젯 파일 수정이 불가능
        # 4 : 파일 이름을 입력하지 않음
        # 5 : 저장할 정보가 없음
        # 6 : 저장 파일을 생성할 수 없음
        # 7 : 저장 폴더에 접근할 수 없거나, 파일을 찾을 수 없음
        # 8 : 저장 파일을 불러올 수 없음
        message = ""
        if (error_no == 1) :
            message = "기본 위젯 파일에 접근할 수 없습니다."
        elif (error_no == 2) :
            message = "해당 위젯 파일이 이미 존재합니다."
        elif (error_no == 3) :
            message = "기본 위젯 파일을 수정할 수 없습니다."
        elif (error_no == 4) :
            message = "파일 이름이 입력되지 않았습니다."
        elif (error_no == 5) :
            message = "저장할 위젯이 없습니다."
        elif (error_no == 6) :
            message = "저장 파일을 생성할 수 없습니다."
        elif (error_no == 7) :
            message = "저장 파일을 찾을 수 없습니다."
        elif (error_no == 8) :
            message = "저장 파일을 불러올 수 없습니다."
        else :
            message = "알수 없는 오류가 발생했습니다."

        label = self.dialog_error.findChild(Header.QLabel)
        label.setText(message)
        self.dialog_error.exec_()


    def makeNewWidgetFile(self) :
        # 위젯 파일 경로에서 default.py 확인
        list_python_files = []
        try :
            list_resources = Header.os.listdir(self.path_widgetfile)
            list_python_files = list(f for f in list_resources if f.endswith(".py")) # .py 파일 전부 확인
        except :
            # 위젯 파일 디렉토리에 접근 불가능
            self.showErrorDialog(1)
            return

        path_default = None
        # 파이썬 파일 리스트에서 각 파일을 모듈로 임포트하여 (name, module)의 리스트인 list_widget_file 제작
        for file_py in list_python_files :
            t_name = file_py[:-3] # 파일 이름에서 .py 제거 -> 모듈 이름
            if t_name == "default" : # 기본 파일 default를 찾은 경우
                path_default = self.path_widgetfile + "\\default.py"

        if not path_default : # default.py를 찾지 못한 경우
            self.showErrorDialog(1)
            return

        # 다이얼로그 설정을 변경하고 실행
        self.showFileSelectDialog(1)
        if self.need_to_get_filename : # 다이얼로그에서 확인 버튼이 입력된 경우
            lineedit = self.dialog_file_select.findChild(Header.QLineEdit)
            filename = lineedit.text()
            if not filename : # 입력값이 없는 경우
                self.showErrorDialog(4)
                return
            
            path_new = self.path_widgetfile + "\\" + filename + ".py"
            for file_py in list_python_files :
                t_name = file_py[:-3]
                if t_name == filename : # 이름이 같은 위젯 파일이 이미 존재하는 경우
                    self.showErrorDialog(2)
                    return

            # default.py에서 default 를 filename으로 변경한 후 새로운 파일 생성
            file_new = open(path_new, 'w', encoding="utf-8") # 파일 생성
            try :
                with Header.fileinput.FileInput(path_default, openhook=Header.fileinput.hook_encoded("utf-8")) as f :
                    for line in f :
                        if "default" in line :
                            line = line.replace("default", filename) # 파일에 등장하는 default를 filname으로 변경
                        file_new.write(line) # default를 한줄 씩 옮겨 작성
            except :
                self.showErrorDialog(3)
                return
            file_new.close()
            Header.os.popen(path_new)

    def clickedDialogOk(self, t_or_f) :
        self.need_to_get_filename = t_or_f
        self.dialog_file_select.close()

    def makeFileSelectDialog(self) :
        dialog = Header.QDialog(self, Header.Qt.WindowTitleHint | Header.Qt.WindowCloseButtonHint)
        dialog.setWindowTitle("파일 이름 입력")
        dialog.setFixedWidth(300)
        dialog.setFixedHeight(120)

        label_message = Header.QLabel("", dialog)
        label_message.setFont(self.error_font)
        label_message.setFixedSize(280, 30)
        label_message.setAlignment(Header.Qt.AlignLeft)
        label_message.move(15, 10)

        label_input = Header.QLineEdit("", dialog)
        label_input.setFont(self.error_font)
        validator = Header.QRegExp("[0-9a-zA-Z]+") # 파일 이름은 영문과 숫자만 허용
        label_input.setValidator(Header.QRegExpValidator(validator))
        label_input.setFixedSize(260, 30)
        label_input.move(20, 45)

        button_ok = Header.QPushButton("확인", dialog)
        button_ok.setFont(self.error_font)
        button_ok.setFixedSize(100, 30)
        button_ok.move(70, 85)
        button_ok.clicked.connect(lambda : self.clickedDialogOk(True))

        button_cancel = Header.QPushButton("취소", dialog)
        button_cancel.setFont(self.error_font)
        button_cancel.setFixedSize(100, 30)
        button_cancel.move(180, 85)
        button_cancel.clicked.connect(dialog.close)

        return dialog

    def showFileSelectDialog(self, type) :
        message = ""
        label = self.dialog_file_select.findChild(Header.QLabel)
        lineedit = self.dialog_file_select.findChild(Header.QLineEdit)
        lineedit.setText("")
        # type
        # 1 : 새 위젯 파일 생성
        # 2 : 저장 파일 생성
        # 3 : 불러올 파일 지정
        if type == 1 :
            message = "생성할 위젯 파일의 이름을 입력하세요."
        elif type == 2 :
            message = "저장 파일의 이름을 입력하세요."
        elif type == 3 :
            message = "불러올 파일의 이름을 입력하세요."
        else :
            return # type이 잘못 지정된 경우, 아무것도 실행하지 않음

        self.need_to_get_filename = False
        label.setText(message)
        self.dialog_file_select.exec_()

    def saveProgram(self) :
        # programing에 모든 위젯 정보 요청
        self.signal_request_data.emit()

    def saveData(self, list_data_widget) :
        # 위젯 정보를 파일 형태로 저장
        if not list_data_widget : # 저장할 정보가 없는 경우
            self.showErrorDialog(5)
            return
        # 저장 파일의 이름 입력
        self.showFileSelectDialog(2)
        if self.need_to_get_filename : # 다이얼로그에서 확인 버튼이 입력된 경우
            lineedit = self.dialog_file_select.findChild(Header.QLineEdit)
            filename = lineedit.text()
            if not filename : # 입력값이 없는 경우
                self.showErrorDialog(4)
                return
            # filname.bin 파일을 생성하여 데이터 저장
            path_file = self.path_savefile + "\\" + filename + ".bin"
            savefile = None
            try :
                savefile = open(path_file, "wb")
            except :
                if savefile :
                    savefile.close()
                self.showErrorDialog(6)
                return
            # pickle을 통해 암호화하여 저장
            try :
                Header.pickle.dump(list_data_widget, savefile)
                savefile.close()
            except :
                if savefile :
                    savefile.close()
                self.showErrorDialog(6)
                return

    def loadProgram(self) :
        filename = ""
        # 저장 파일의 이름 입력
        self.showFileSelectDialog(3)
        if self.need_to_get_filename : # 다이얼로그에서 확인 버튼이 입력된 경우
            lineedit = self.dialog_file_select.findChild(Header.QLineEdit)
            filename = lineedit.text()
            if not filename : # 입력값이 없는 경우
                self.showErrorDialog(4)
                return
            # filname.bin을 탐색
            path_file = self.path_savefile + "\\" + filename + ".bin"
            list_bin_files = []
            savefile = None
            try :
                if not Header.os.path.exists(path_file) : # 저장파일이 존재하지 않는 경우
                    self.showErrorDialog(7)
                    return
                else :
                    savefile = open(path_file, "rb") # 저장 파일 열기
            except :
                if savefile :
                    savefile.close()
                self.showErrorDialog(7)
                return
            list_data_widget = []
            try :
                list_data_widget = Header.pickle.load(savefile) # 파일 데이터 로드
                savefile.close()
            except : 
                if savefile :
                    savefile.close()
                self.showErrorDialog(8)
                return
            if list_data_widget :
                # 저장파일 데이터를 programming에 전송하여 위젯 생성
                self.signal_pass_data_to_programming.emit(list_data_widget)
            else :
                self.showErrorDialog(8)
                return



    