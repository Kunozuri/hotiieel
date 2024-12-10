from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, QThreadPool, QRunnable
from database import SQLConnector

class SignUp(QWidget):
    def __init__(self, landing_page: object=None, login_page: object=None, parent:object = None):
        super(SignUp, self).__init__(parent)
        
        self.__background_run = QThreadPool()
        
        self.landing_page = landing_page
        self.login_page = login_page
        
        self.settings()
        self.initUI()
        
    def initUI(self):
        
        master_layout = QVBoxLayout()
        r0w1 = QHBoxLayout()
        
        # -- buttons initialization -- #
        logo = self.landing_page.button001(font="Lato")
        back = self.login_page.back_button()
        register = self.landing_page.button002(text="Register", bg_color="#000000", text_color="white")
        
        # -- buttons clicked -- #
        logo.clicked.connect(self.logo)
        back.clicked.connect(self.back)
        register.clicked.connect(self.register)
        
        # -- input bar initialization -- #
        self.username = self.landing_page.input_box("Username", bg_color="#FFFFFF", width= 500, height=50)
        self.password = self.landing_page.input_box("Password", bg_color="#FFFFFF", width= 500, height=50)
        self.first_name = self.landing_page.input_box("Firstname", bg_color="#FFFFFF", width= 500, height=50)
        self.last_name = self.landing_page.input_box("Lastname", bg_color="#FFFFFF", width= 500, height=50)
        self.email = self.landing_page.input_box("Email", bg_color="#FFFFFF", width= 500, height=50)
        self.phone = self.landing_page.input_box("Phone", bg_color="#FFFFFF", width= 500, height=50)
        self.address = self.landing_page.input_box("Address", bg_color="#FFFFFF", width= 500, height=50)
        self.birthday = self.landing_page.input_box("Birthday", bg_color="#FFFFFF", width= 500, height=50)

        master_layout.addSpacing(30)
        master_layout.addWidget(back, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        master_layout.addWidget(logo, alignment=Qt.AlignmentFlag.AlignCenter)
        master_layout.addWidget(self.username, alignment=Qt.AlignmentFlag.AlignCenter)
        master_layout.addWidget(self.password, alignment=Qt.AlignmentFlag.AlignCenter)
        master_layout.addSpacing(20)
        master_layout.addWidget(self.first_name, alignment=Qt.AlignmentFlag.AlignCenter)
        master_layout.addWidget(self.last_name, alignment=Qt.AlignmentFlag.AlignCenter)
        master_layout.addWidget(self.email, alignment=Qt.AlignmentFlag.AlignCenter)
        master_layout.addWidget(self.phone, alignment=Qt.AlignmentFlag.AlignCenter)
        master_layout.addWidget(self.address, alignment=Qt.AlignmentFlag.AlignCenter)
        master_layout.addWidget(self.birthday, alignment=Qt.AlignmentFlag.AlignCenter)
        master_layout.addSpacing(30)
        
        master_layout.addWidget(register, alignment=Qt.AlignmentFlag.AlignCenter)
        master_layout.addSpacing(50)
        
        self.setLayout(master_layout)
    
    
    def register(self):
        """ Register the guest and bring you back directly to login page """
        
        username = self.username.text().strip()
        password = self.password.text().strip()
        firstname = self.first_name.text().strip()
        lastname = self.last_name.text().strip()
        email = self.email.text().strip()
        phone = self.phone.text().strip()
        address = self.address.text().strip()
        birthday = self.birthday.text().strip()

        this_db = SQLConnector(method= "add_guest", parameters= {
            "username": username,
            "password": password,
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "phone": phone,
            "address": address,
            "birthday": birthday
            
            }
        )
        
        helper = self.run_in_background(this_db, "add_guest")

        self.__background_run.start(helper)

        self.__background_run.waitForDone() # Wait for the background task to complete before proceeding
        
        self.hide()
        self.login_page.show()
    
    def settings(self):
        """ Settings of the sign up page UI """
        self.setWindowTitle("zrsmyley--Landing Page")
        self.setGeometry(100, 100, 1366, 768)
        
    def back(self) -> None:
        """ Back button to bring you back to the landing page """
        self.hide()
        self.landing_page.show()
        
    def logo(self) -> None:
        """ logo button to bring you back to the landing page """
        self.hide()
        self.landing_page.show()
        
    def run_in_background(self, Object_to_run, method_to_run):
        """ Helper function to run an Object in background """
        result = Helper(Object_to_run, method_to_run)
        return result
    
class Helper(QRunnable):
    def __init__(self, blueprint, methods):
        super().__init__()
        self.__object = blueprint
        self.__method = methods
        self.result = None  # Container for the result

    def run(self):
        method = getattr(self.__object, self.__method, None)
        if callable(method):
            self.result = method(self.__object.parameters)