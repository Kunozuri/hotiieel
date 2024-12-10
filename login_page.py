from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QCheckBox)

class Login(QWidget):
    def __init__(self, landing_page: object= None, admin: object= None, parent= None):
        super(Login, self).__init__(parent)
        
        self.__landing_page = landing_page # composition
        self.__admin = admin
        
        self.settings()
        self.initUI()
        
    def initUI(self):
        
        master_layout = QVBoxLayout()
        last_row = QHBoxLayout()
        
        back = self.back_button()
        back.clicked.connect(self.back)
        
        logo = self.__landing_page.button001(size=50, font="Lato")
        notice = self.__landing_page.text_label("refrain from using your real password as I didnt put much attention into security", color="000000", size=12)
        username = self.__landing_page.input_box("Username", bg_color="#FFFFFF", width=500, height=70)
        password = self.__landing_page.input_box("Password", bg_color="#FFFFFF", is_password=True, width=500, height=70)
        remember_me = QCheckBox("Remember me")
        forgot_password = self.__landing_page.button001("Forgot password?")
        login = self.__landing_page.button002(text="Login", bg_color="#000000", text_color="white")
        
        login.clicked.connect(self.login)
        
        master_layout.addWidget(back)
        master_layout.addWidget(logo, alignment=Qt.AlignmentFlag.AlignCenter)
        master_layout.addWidget(notice, alignment=Qt.AlignmentFlag.AlignCenter)
        master_layout.addWidget(username, alignment=Qt.AlignmentFlag.AlignCenter)
        master_layout.addWidget(password, alignment=Qt.AlignmentFlag.AlignCenter) 
        
        last_row.addWidget(remember_me)
        last_row.addWidget(forgot_password)
        
        master_layout.addLayout(last_row)
        
        master_layout.addWidget(login, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(master_layout)
    
    def settings(self):
        self.setWindowTitle("zrsmyley--Landing Page")
        self.setGeometry(100, 100, 1366, 768)
       
    def back_button(self, text: str= "Back", width: int= 100, height: int=40, alignment: object=Qt.AlignmentFlag.AlignLeft) -> QPushButton:
        this_button = QPushButton(text)
        this_button.setFixedSize(width, height)
        this_button.setStyleSheet("""
            background-color: black;
            border-radius: 20px;
            color: white;
        """)
        
        return this_button
    
    def back(self):
        self.hide()
        self.__landing_page.show()
    
    def login(self):
        self.hide()
        self.__admin.show()