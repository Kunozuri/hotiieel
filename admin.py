from PyQt5.QtWidgets import (
    QApplication, QTableWidgetItem, QGridLayout, QLineEdit, QVBoxLayout, QLabel, QWidget, QPushButton, QHBoxLayout, QHeaderView, QTableWidget
)
from PyQt5.QtCore import QThreadPool
from database import SQLConnector
from sign_up_page import SignUp

class Admin(QWidget):
    def __init__(self, landing_page: object= None, parent= None):
        super(Admin, self).__init__(parent= None)
        
        self.__table_list = ["transaction", "guest", "room", "reservation", "auth"]
        self.current_table_name = "reservation"
        self.__current_table = None
        
        self.background_run = QThreadPool()
        
        self.__landing_page = landing_page
        self.to_run_in_background = SignUp
        self.edit_form = EditForm(self, self.current_table_name)
        
        self.settings()
        self.initUI()

    def initUI(self) -> None:
        master_layout = QVBoxLayout()
        
        row01 = self.app_bar()
        row02 = QHBoxLayout()
        
        navigation_text = "View Transactions" if self.current_table_name == "reservation" else "Back"
        
        navigation = QPushButton(navigation_text)
        edit = QPushButton("Edit")
        
        navigation.clicked.connect(self.navigation)
        edit.clicked.connect(self.edit)
        
        table = self.table_on_display() if not self.__current_table else self.__current_table # switch between customized table and whole table content
        
        heads = table.horizontalHeader()
        heads.sectionClicked.connect(self.headers)

        row02.addWidget(navigation)
        row02.addWidget(edit)
        
        master_layout.addWidget(row01)
        master_layout.addLayout(row02)
        master_layout.addWidget(table)
        
        self.setLayout(master_layout)
    
    def app_bar(self) -> QWidget:
        app_bar = QWidget()
        app_bar.setMinimumSize(1360, 150)
        app_bar.setStyleSheet("""
        background-color: #cccccc;
        border-radius: 20px;
        """)
        
        master_layout = QVBoxLayout(app_bar)
        row01 = QHBoxLayout()
        row02 = QHBoxLayout()
        
        logo = QLabel("Zrsmyley")
        logout = QPushButton("Logout")
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText(f"Search the {self.current_table_name} {'username' if self.current_table_name == 'guest' else 'ID'}")
        
        search = QPushButton("Search")
        
        logout.clicked.connect(self.logout)
        search.clicked.connect(self.search)
        
        row01.addWidget(logo)
        row01.addWidget(logout)
        row02.addWidget(self.search_bar)
        row02.addWidget(search)
        
        master_layout.addLayout(row01)
        master_layout.addLayout(row02)
        
        return app_bar

# -- GETTERS -- #
    def tables(self, table_name) -> QTableWidget:
        """ this create the table and populate it directly """
        
        # This area needs to debug in other device TAKE NOTE!
        
        # -- getting data from database  -- #
        content = self.access_database(method= "get_table_content", parameter= table_name)

        print(f"hello {content.result}") # delete this after your debugging we dont need shit lines
        #data, table_header = content.result
        
        data, table_header = [],[] # delete this , this is only for satisfying to not have errors
        
        table = self.populate_table(data, table_header)
        
        return table

# -- SYSTEM -- #
    def settings(self) -> None:
        self.setWindowTitle("zrsmyley -- Admin")
        self.setGeometry(100, 100, 1366, 768)

# -- EVENTS -- #
    def logout(self) -> None:
        self.hide()
        self.__landing_page.show()

    def search(self) -> None:
        from_this = "username" if self.current_table_name == "guest" else f"{self.current_table_name}_id"
        look_for = self.search_bar.text()
        
        content = self.access_database(
            method= "get_searched",
            parameter= {
                "from_this": from_this, 
                "look_for": look_for, 
                "table_name": self.current_table_name
                }
            )
        data, table_header = content.result
        
        
        #data, table_header = [],[] # delete this , this is only for satisfying to not have errors
        
        self.__current_table = self.populate_table(data, table_header)
        self.search_bar.clear()
    
    def edit(self) -> None:
        self.hide()
        self.edit_form.show()
         
# -- CONTROL FLOW EVENTS -- #
    def navigation(self) -> None:
        """ if the back button gets clicked"""
        if self.current_table_name in self.__table_list[2::-1] and self.__current_table == None:
            self.current_table_name = "reservation"
        elif self.current_table_name in self.__table_list[3] and self.__current_table == None:
            self.current_table_name = "transaction"
        elif self.current_table_name == "authentication" and self.__current_table == None:
            self.current_table_name = "guest"
        else:
            self.__current_table = None
        
    def headers(self, index: int) -> None:
        """ if the headers gets clicked"""
        match self.current_table_name:
            case "reservation":
                match index:
                    case 1:
                        self.current_table_name = "guest"
                    case 2:
                        self.current_table_name = "room"
            case "guest":
                match index:
                    case 1:
                        self.current_table_name = "auth"
            case "transaction":
                match index:
                    case 1:
                        self.current_table_name = "reservation" 

    def table_on_display(self) -> QTableWidget:
        """ HELPER: Will monitor which or what table to display """
        table = None
        
        for table_name in self.__table_list:
            if table_name == self.current_table_name and self.__current_table == None:
                table = self.tables(self.current_table_name)
            elif table_name == "auth" and self.__current_table == None:
                table = self.tables(self.current_table_name)
            
            if self.__current_table != None or table_name == self.current_table_name:
                break
        else:
            table = self.__current_table
        
        return table
    """ ATTENTION: if not works on changing the table then try this inserting inside the button clicked functions"""

# -- HELPERS -- #   
    def populate_table(self, data: list, table_header: list) -> QTableWidget:
        """ HELPER: Will return a new set of table """
        
        # -- displaying header into table -- #
        table = QTableWidget(0,len(table_header))
        table.setHorizontalHeaderLabels(table_header)
        
        #table = QTableWidget(0,1) # to be deleted
        #table.setHorizontalHeaderLabels(['hello']) # to be deleted
         
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)    
        
        # -- displaying data into table -- #
        for row_idx, row_data in enumerate(data):
            for col_idx, value in enumerate(row_data):
                table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        
        return table

    def access_database(self, method, parameter):
        """ HELPER: That will access data from Database aswell as Run a specified method from the SQLConnector class """
        
        this_db = SQLConnector(method, parameter)
        table_content = self.to_run_in_background.run_in_background(None, Object_to_run= this_db, method_to_run= this_db.method)
        self.background_run.start(table_content)
        self.background_run.waitForDone()

        return table_content


class EditForm(QWidget):
    def __init__ (self, admin: object, current_table: str, parent= None):
        super(EditForm, self).__init__(parent= None)
        
        self.background_run = QThreadPool()
        
        self.__admin = admin
        
        self.__current_table = current_table
        self.__table_header = self.__admin.access_database("get_attribute_header", self.__current_table)
        
        self.__inputs = {}
        
        self.settings()
        self.initUI()
    
    def initUI(self) -> None:
        master_layout = QVBoxLayout()
        buttons = QHBoxLayout()
        
        grid = QGridLayout()
        
        for row, header in enumerate(self.__table_header.result):
            data = QLineEdit()
            data.setPlaceholderText(f"Enter {header}")
            
            self.__inputs[header] = data
            
            grid.addWidget(data, row, 0)
        
        add = QPushButton("Add")
        remove = QPushButton("Remove")
        done = QPushButton("Done")
        
        add.clicked.connect(self.add)
        remove.clicked.connect(self.remove)
        #done.clicked.connect(self.done)
        
        buttons.addWidget(add)
        buttons.addWidget(remove)
        
        master_layout.addLayout(grid)
        master_layout.addLayout(buttons)

    
        
        
        # get the table header and used it into the Qlineedit
        # the Qlineedit must loop depending on the lenght of the header
        # if it click add the the data should be added
        # remove the data otherwise if clicked the remove
        # use menu to navigate through table admin desire to modify
    
    def add(self) -> None:
        
        data = self.input_value()
        
        table = f"add_{self.__current_table}"
        result = self.__admin.access_database(table, data)
        
        if not result:
            match self.__current_table:
                case "transaction":
                    self.__current_table = "reservation"
                case "guest":
                    self.__current_table = "reservation"
                case "room":
                    self.__current_table = "reservation"
                case "authentication":
                    self.__current_table = "guest"
    
    def remove(self) -> None:
        # Get the input values
        data = self.input_value()  # Ensure this returns a dictionary
        if not data:
            print("No data provided.")
            return

        # Extract the first key-value pair (assuming only one is needed)
        key, value = next(iter(data.items()))

        # Perform the deletion operation
        try:
            self.__admin.access_database("remove_data", key, value)
            print(f"Successfully removed entry where {key} = {value}.")
        except Exception as e:
            print(f"Error during removal: {e}")

    def back(self) -> None:
        self.hide()
        self.__admin.show()
        
    def settings(self) -> None:
        self.setWindowTitle("zrsmyley -- Admin")
        self.setGeometry(100, 100, 1366, 768)

    def input_value(self):
        """ GETTER: Will get the data of user input that will be added or remove"""
        data = {}
        for header, value in self.__inputs.items():
            data[header] = value.text()
        return data

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    # Show the main window
    window = Admin()
    window.show()

    sys.exit(app.exec_())