import sys
from PyQt5.QtWidgets import QApplication
from landing_page import Landing
from login_page import Login
from sign_up_page import SignUp
from admin import Admin

class HotelStructure:
    def __init__(self):
            
        self.landing_page = Landing()
        self.admin = Admin(self.landing_page)
        self.login_page = Login(self.landing_page, self.admin)
        self.sign_up_page = SignUp(self.landing_page, self.login_page)
        
        # -- References to Landing Page -- #
        self.login_page.landing_page = self.landing_page
        self.admin.landing_page = self.landing_page
        
        # -- References to Login Page -- #
        self.landing_page.login_page = self.login_page
        
        # -- References to Sign Up Page -- #
        self.landing_page.sign_up_page = self.sign_up_page
        
        # -- References to Admin -- #
        self.login_page.admin = self.admin
        
        self.landing_page.show()

def main():
    app = QApplication(sys.argv)
    HotelStructure()

    result = app.exec_()
    sys.exit(result)

if __name__ == "__main__":
    main()