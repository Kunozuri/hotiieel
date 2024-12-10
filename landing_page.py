from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QScrollArea, QLineEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class Landing(QWidget):
    """This where you be when you open the desktop when you're yet logged in"""    
    def __init__(self, parent = None):
        super(Landing, self).__init__(parent)
        
        self.settings()
        self.initUI()

    def initUI(self) -> None:
        main_layout = QVBoxLayout() # where landing page scroll area is attached
        
        landing_page_scroll_area = self.scroll_area() # where you scroll through the landing page content
        
        scroll_content = QWidget() # content widget inside the scroll area
        scroll_layout = QVBoxLayout(scroll_content) # master layout of the content area

        self.first_row() # first row where login and sign-up button located        
        self.second_row() # second row where welcome message is located
        self.third_row() # third row where arrow button is located
        
        # where rows are added to content master layout
        scroll_layout.addLayout(self.first_row())
        scroll_layout.setSpacing(35)
        scroll_layout.addWidget(self.second_row())
        scroll_layout.addLayout(self.third_row())
        
        landing_page_scroll_area.setWidget(scroll_content) # where the whole content gets bind into scroll area
        main_layout.addWidget(landing_page_scroll_area) # where the scroll area get added to the main layout
        self.setLayout(main_layout) # where we publish the main layout to be visible

    def first_row(self) -> QHBoxLayout:
        r0w1 = QHBoxLayout()

        # button widgets set-up
        zrsmyley = self.button001(size=35, font="Lato")
        properties = self.button001("Properties")
        attractions = self.button001("Attractions")
        popular = self.button001("Popular")
        login = self.button002("Login", bg_color="#000000", text_color="white")
        signUp = self.button002("Sign Up")
        
        # buttons clicked
        login.clicked.connect(self.login_button_clicked)
        signUp.clicked.connect(self.signUp_button_clicked)
        
        # adding button widgets to layout
        r0w1.addWidget(zrsmyley)
        r0w1.addWidget(properties)
        r0w1.addWidget(attractions)
        r0w1.addWidget(popular)
        r0w1.addStretch()
        r0w1.addWidget(signUp)
        r0w1.addWidget(login)
        
        return r0w1

    def second_row(self) -> QWidget:
        r0w2_widget = self.custom_widget(width=1325) # row 2 main widget in the scroll bar
        r0w2 = QVBoxLayout(r0w2_widget) # master layout in row 2 widget
        
        # welcome cover set-up
        welcome_text = self.text_label("Book your stay with Zrsmyley", size=28)
        invite_text = self.text_label("16 luxurius rooms are waiting for you!")
        
        # making welcome cover visible
        r0w2.addWidget(welcome_text)
        r0w2.addWidget(invite_text)
        
        # below was another widget inside the current widget, just like nested control flow
        nested_widget = self.custom_widget(height=90, width=700, background="#FFFFFF", radius=39)
        
        # nested layout structure
        nested_r0w_master = QHBoxLayout(nested_widget) 
        nested_r0w_v1 = QVBoxLayout()
        nested_r0w_v2 = QVBoxLayout()
        nested_r0w_v3 = QVBoxLayout()
        nested_r0w_v4 = QVBoxLayout()
        
        # label set-up
        address_label = self.text_label("Address", size=12 ,color="#000000")
        check_in_label = self.text_label("Check-in", size=12, color="#000000")
        check_out_label = self.text_label("Check-out", size=12, color="#000000")
        guest_label = self.text_label("Guests", size=12, color="#000000")
        
        # input box set-up
        address_box = self.input_box("Where are you from?")
        check_in_box = self.input_box("Add date")
        check_out_box = self.input_box("Add date")
        guest_box = self.input_box("Number of guests")
        
        # adding the label into the first row of the child widget
        nested_r0w_v1.addWidget(address_label, alignment=Qt.AlignmentFlag.AlignLeft)
        nested_r0w_v2.addWidget(check_in_label, alignment=Qt.AlignmentFlag.AlignLeft)
        nested_r0w_v3.addWidget(check_out_label,  alignment=Qt.AlignmentFlag.AlignLeft)
        nested_r0w_v4.addWidget(guest_label,  alignment=Qt.AlignmentFlag.AlignLeft)

        # adding the input box into the second row of the child widget
        nested_r0w_v1.addWidget(address_box)
        nested_r0w_v2.addWidget(check_in_box)
        nested_r0w_v3.addWidget(check_out_box)
        nested_r0w_v4.addWidget(guest_box)
        
        # arrow button
        arrow_button = self.button002(
            text="➔",
            width=70,
            heigth=60,
            bg_color="#000000",
            text_color="white",
            radius=30)
        
        # buttons clicked
        arrow_button.clicked.connect(self.login_button_clicked)
        
        # adding the two row into the master layout which is the culomn
        nested_r0w_master.addLayout(nested_r0w_v1)
        nested_r0w_master.addLayout(nested_r0w_v2)
        nested_r0w_master.addLayout(nested_r0w_v3)
        nested_r0w_master.addLayout(nested_r0w_v4)
        nested_r0w_master.addWidget(arrow_button)
        
        r0w2.addWidget(nested_widget, alignment=Qt.AlignmentFlag.AlignCenter) # add the child widget into the parent widget
        
        return r0w2_widget
    
    def third_row(self) -> QHBoxLayout:
        r0w3 = QHBoxLayout()
        kahubyaan = self.text_label("designan ko in later", color="000000", size=30)
        kahubyaan.setAlignment(Qt.AlignmentFlag.AlignCenter)
        r0w3.addWidget(kahubyaan)
        
        return r0w3
    
    # -- windows settings -- #
    def settings(self) -> None:
        """ settings of the landing page window """
        
        self.setWindowTitle("zrsmyley--Landing Page")
        self.setGeometry(100, 100, 1366, 768)
    
    # -- 
    def custom_widget(self, background: str="#cccccc", radius: int=20, height: int=250, width: int=250) -> QWidget:
            """ just in case you need a new widget """
            
            this_widget = QWidget()
            this_widget.setFixedSize(width, height)
            this_widget.setStyleSheet(f"""
                background-color: {background};
                border-radius: {radius}px;
                """)
                
            return this_widget
    
    # -- line edits -- #             
    def input_box(self, place_holder: str= "defualt", bg_color: str= "transparent", border: str="none", width: int=120, height: int=20, is_password: bool=False) -> QLineEdit:
        """ input box baby """
        
        this_box = QLineEdit()
        this_box.setPlaceholderText(place_holder)
        this_box.setFixedSize(width, height)
        
        if is_password:
            this_box.setEchoMode(QLineEdit.EchoMode.Password)
        
        this_box.setStyleSheet(f"""
            border: {border};
            background-color: {bg_color};
        """)
        
        return this_box
    
    # -- scroll bar -- #
    def scroll_area(self) -> QScrollArea:
        """ scroll area for you to navigate the content """
        
        this_scroll_area = QScrollArea()
        this_scroll_area.setWidgetResizable(True) # so that it follows the windows size
        this_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Hide vertical scroll bar
        this_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff) # Hide horizontal scroll bar
        this_scroll_area.setFocusPolicy(Qt.StrongFocus) # idk what this means basta gin gpt ko in 
        this_scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
            }
        """)
        
        return this_scroll_area
    
    # -- label prototype -- #
    def text_label(self, text: str = "default", font: str = "Times New Roman", color: str= "#FFFFFF", size: int = 15, alignment: object= Qt.AlignmentFlag.AlignCenter, isBold: bool = False) -> QLabel:
        """ label muna bago gawan ng website resume, tsk, tsk, tsk! """
        
        this_label = QLabel(text)
        this_label.setAlignment(alignment)        
        
        label_font = QFont(font, size)
        this_label.setFont(label_font)
        
        if isBold:
            label_font.setBold(True)
        else:
            label_font.setBold(False)
            
        this_label.setStyleSheet(f"""
            color: {color};
            background-color: none;
            padding: 10px;
            border-radius: none;
            font-weight: {'bold' if isBold else 'normal'};
        """)

        return this_label
    
    # -- buttons prototype -- #
    def button001(self, text: str= "Zrsmyley", text_color: str= "#000000", size: int= 20, font: str="Times New Roman") -> QPushButton:
        """ first button prototype """
        
        size_and_font = f"{str(size)}px {font}"
        this_button = QPushButton(text)
        this_button.setStyleSheet(f"""
            QPushButton {{
                border: none;
                background: none;
                color: {text_color};
                font: {size_and_font};
            }}
        """)
        
        return this_button

    def button002(self, text: str="defualt", width: int=150, heigth: int=40, radius: int=20, bg_color: str= "#FFFFFF", text_color: str="black", font: str="Poppins" ) -> QPushButton:
        """ second button prototype """
        
        this_button = QPushButton(text)
        this_button.setFixedSize(width, heigth)
        
        this_button.setStyleSheet(f"""
            QPushButton {{
                border: 1px solid #000000;
                border-radius: {radius}%;
                background-color: {bg_color};
                color: {text_color};
                font-size: 16px;
                font-family: {font}
            }}
        """)

        return this_button

    # -- buttons clicked -- #
    def login_button_clicked(self) -> None:
        self.hide()
        self.login_page.show()
        
    def signUp_button_clicked(self) -> None:
        self.hide()
        self.sign_up_page.show()
