import mysql.connector
from mysql.connector import Error
from PyQt5.QtCore import QRunnable

class SQLConnector(QRunnable):
    def __init__(self, method: str= "run", parameters: dict={}):
        """ connection to database can only be modify here """
        self.__host= "localhost"
        self.__user= "root"
        self.__port= 3307
        self.__passwd= "admin"
        
        self.parameters = parameters # expected parameter of every method
        self.method = method # method to run
        
        self.__connection = None

# -- DEFAULTS -- #
    def run(self) -> None:
        print("You are caliing the default run.\nDid you perhaps forgot to especify the method to run?.")

# -- ACCESSORS -- #
    def __connect_db(self) -> None:
        """Establish a connection to the database."""
        sql = """
            CREATE DATABASE IF NOT EXISTS hotel_reservation;
        """
        try:
            print("Trying to connect.")
            self.__connection = mysql.connector.connect(
                host= self.__host,
                user= self.__user,
                port= self.__port,
                passwd= self.__passwd,
            )
            if self.__connection.is_connected():
                self.execute_sql(sql)
                self.__connection.database= "hotel_reservation"
                print("Connection to the database was successful.")
        
        except Error as e:
            print(f"Error while connecting to the database: {e}")
            
    def __disconnect_db(self) -> None:
        """Close the database connection."""
        if self.__connection is not None and self.__connection.is_connected():
            self.__connection.close()
            print("Database connected.")

# -- EXECUTORS, EYYYYY! -- #
    def execute_sql(self, sql: str, value= None) -> None:
        """ Helper to execute SQL for (INSERT, UPDATE, DELETE). """
        
        if self.__connection is None or not self.__connection.is_connected():
            print("Connection is not established.")
            return

        cursor = self.__connection.cursor()
        try:
            cursor.execute(sql, value)
            self.__connection.commit()
            print("Query executed successfully.")
        except Error as e:
            print(f"Error executing query: {e}")
            self.__connection.rollback()
        finally:
            cursor.close()

    def fetch_sql(self, sql: str, value: None) -> list:
        """Helper execute a (SELECT) SQL and return its results."""
        if self.__connection is None or not self.__connection.is_connected():
            print("Connection is not established.")
            return None

        cursor = self.__connection.cursor()
        try:
            cursor.execute(sql, value)
            results = cursor.fetchall()
            return results
        except Error as e:
            print(f"Error fetching data: {e}")
            return None
        finally:
            cursor.close()
    
# -- ADD -- #
    def add_guest(self, guest_info):
        """ will append the guest information into the guest table of the database hotel """
        username = guest_info["username"]
        password = guest_info["password"]
        firstname = guest_info["firstname"]
        lastname = guest_info["lastname"]
        email = guest_info["email"]
        phone = guest_info["phone"]
        address = guest_info["address"]
        birthday = guest_info["birthday"]
        
        sql = """
                INSERT INTO guest (username, firstname, lastname, email, phone, address, birthday)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """
        value = (username, firstname, lastname, email, phone, address, birthday)
        
        result = self.check_if_exists(tablename= "guest", column= "password", id_checking= password)
        if not result:
            return False
        
        self.__connect_db()
        try:
            self.__creat_guest_table()
            self.add_password(password)
            self.execute_sql(sql, value)
        except Exception as E:
            print(f"Insertion error: {E}")
        
        finally:    
            self.__disconnect_db()
            print("Data has been addeed.")
    
    def add_password(self, password):
        """ will append the guest information into the guest table of the database hotel """
        sql = """
                INSERT INTO authentication (password)
                VALUES (%s);
            """
        value = (password)
        self.__connect_db()
        try:
            self.__create_authentication()
            self.execute_sql(sql, value)
        except Exception as E:
            print(f"Insertion error: {E}")
        
        finally:    
            self.__disconnect_db()
            print("Data has been addeed.")

    def add_reservation(self, reservation_info):
        """ will append the guest information into the guest table of the database hotel """
        reservation_id = reservation_info["reservation_id"]
        username = reservation_info["username"]
        room_id = reservation_info["room_id"]
        check_in_date = reservation_info["check_in_date"]
        check_out_date = reservation_info["check_out_date"]
        status = reservation_info["status"]
        issued_date = reservation_info["issued_date"]
        
        sql = """
                INSERT INTO reservation (reservation_id, username, room_id, , check_in_date, check_out_date, status, issued_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """
        value = (reservation_id, username, room_id, check_in_date, check_out_date, status, issued_date)
        
        result = self.check_if_exists(tablename= "reservation", column= "username", id_checking= username)
        if not result:
            return False
        
        result = self.check_if_exists(tablename= "reservation", column= "room_id", id_checking= room_id)
        if not result:
            return False
        
        self.__connect_db()
        try:
            self.execute_sql(sql, value)
        except Exception as E:
            print(f"Insertion error: {E}")
        
        finally:    
            self.__disconnect_db()
            print("Data has been addeed.")

    def add_room(self, room_info):
        room_id = room_info["room_id"]
        room_type = room_info["room_type"]
        price_per_night = room_info["price_per_night"]
        is_available = room_info["is_available"]
        
        sql = """
                INSERT INTO room (room_id, room_type, price_per_night, is_available)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """
        value = (room_id, room_type, price_per_night, is_available)
        
        self.__connect_db()
        try:
            self.execute_sql(sql, value)
        except Exception as E:
            print(f"Insertion error: {E}")
        
        finally:    
            self.__disconnect_db()
            print("Data has been addeed.")

    def add_transaction(self, transaction_info):
        transaction_id = transaction_info["transaction_id"]
        reservation_id = transaction_info["reservation_id"]
        amount_paid = transaction_info["amount_paid"]
        payment_date = transaction_info["payment_date"]
        payment_method = transaction_info["payment_method"]

        sql = """
                INSERT INTO transaction (transaction_id, reservation_id, amount_paid, payment_date, payment_method)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """
        value = (transaction_id, reservation_id, amount_paid, payment_date, payment_method)
        
        result = self.check_if_exists(tablename= "transaction", column= "reservation_id", id_checking= reservation_id)
        if not result:
            return False 
        
        self.__connect_db()
        try:
            self.execute_sql(sql, value)
        except Exception as E:
            print(f"Insertion error: {E}")
        
        finally:    
            self.__disconnect_db()
            print("Data has been addeed.")

# -- REMOVE -- #
    def remove_data(self, tablename, columname, item):
        sql = f"DELETE FROM {tablename} WHERE {columname} = %s"
        value = (item, )
        
        self.__connect_db()
        try:
            self.execute_sql(sql, value)
        except Exception as E:
            print(f"Deletion error: {E}")
        
        finally:    
            self.__disconnect_db()
            print("Data has been deleted.")

# -- SEARCH -- #
    def check_if_exists(self, tablename, column, id_checking):
        # Use parameterized queries to prevent SQL injection
        sql = f"SELECT 1 FROM {tablename} WHERE {column} = %s LIMIT 1;"

        self.__connect_db()
        try:
            # Pass id_checking as a parameter to avoid SQL injection
            result = self.fetch_sql(sql, (id_checking,))

            # If result is not None, it means the record exists
            if result:
                print(f"ID {id_checking} exists in {tablename}.")
                return True  # Record exists
            else:
                print(f"ID {id_checking} does not exist in {tablename}.")
                return False  # Record does not exist

        except Exception as E:
            print(f"Error while checking if ID exists: {E}")
            return False  # Return False if there's an error
            
        finally:   
            self.__disconnect_db()

# -- GETTER -- #
    def get_attribute_header(self, table_name: str) -> list:
        """ This will return the column names or the header of the table """
        self.__connect_db()
        cursor = None  # Initialize cursor to None
        try:
            cursor = self.__connection.cursor()
            cursor.execute(f"SHOW COLUMNS FROM {table_name};")
            column_names = [row[0] for row in cursor.fetchall()]  # Extract first column (column name)

            return column_names
        except Exception as e:
            print(f"Error occurred while fetching attribute headers: {e}")
            return []  # Return an empty list in case of an error
        finally:
            if cursor:  # Only close if cursor was successfully created
                cursor.close()
            self.__disconnect_db()


    def get_table_content(self, table_name: str) -> list:
        """ GETTER: Will get the table content aswell as the table headers """
        sql = f"""
            SELECT * FROM {table_name};
        """
        self.__connect_db()
        try:
            self.__create_room()
            self.__create_reservation()
            self.__create_transactions()
            result = self.fetch_sql(sql)
            column_header = self.get_attribute_header(table_name)
            print("returning")
            return result, column_header
        
        except Exception as E:
            print(f"Selection error: {E}")
        
        finally:
            self.__disconnect_db()
        
    def get_searched(self, searching) -> list:
        from_this = searching["from_this"]
        look_for = searching["look_for"]
        table_name = searching.get("table_name")
        
        sql = f"""
            SELECT * 
                FROM guest 
                WHERE {from_this} = {look_for};
        """
        self.__connect_db()
        try:
           results = self.fetch_sql(sql)
           column_header = self.get_attribute_header(table_name)
           return results, column_header
       
        except Exception as E:
            print(f"search error: {E} \n perhaps No result of the thing you looking for.")
        
        finally:
            self.__disconnect_db()

# -- SETTER -- #        
    def set_db_connection(self, host: str, port: int, username: str, password: str):
        self.__host = host
        self.__port = port
        self.__user = username
        self.__passwd = password

# -- CREATORS HAHA, NOTHING MUCH HERE -- #
    def __creat_guest_table(self) -> None:
        sql = """
            CREATE TABLE IF NOT EXISTS `guest` (
                `username` VARCHAR(45) NOT NULL,
                `auth_id` INT DEFAULT NULL,
                `firstname` VARCHAR(45) DEFAULT NULL,
                `lastname` VARCHAR(45) DEFAULT NULL,
                `email` VARCHAR(45) DEFAULT NULL,
                `phone` VARCHAR(15) DEFAULT NULL,
                `address` VARCHAR(45) DEFAULT NULL,
                `birthday` DATE DEFAULT NULL,
                PRIMARY KEY (`username`),
                KEY `idx_auth_id` (`auth_id`),
                CONSTRAINT `fk_guest_auth_id`
                    FOREIGN KEY (`auth_id`)
                    REFERENCES `authentication` (`auth_id`));
        """
        self.execute_sql(sql)
        print("table created")
    
    def __create_authentication(self) -> None:
        sql = """
            CREATE TABLE IF NOT EXISTS `authentication` (
                `auth_id` int NOT NULL AUTO_INCREMENT,
                `password` varchar(255) DEFAULT NULL,
                `last_login` datetime DEFAULT NULL,
                `failed_attempt` int DEFAULT '0',
                PRIMARY KEY (`auth_id`)
            );
        """
        self.execute_sql(sql)

    def __create_reservation(self) -> None:
        sql = """
            CREATE TABLE IF NOT EXISTS `reservation` (
                `reservation_id` INT NOT NULL AUTO_INCREMENT,
                `username` VARCHAR(45) NOT NULL,
                `room_id` INT NOT NULL,
                `check_in_date` DATE NOT NULL,
                `check_out_date` DATE NOT NULL,
                `status` ENUM('confirmed', 'cancelled', 'pending') DEFAULT 'pending' NOT NULL,
                `issued_date` DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (`reservation_id`),
                INDEX `username_idx` (`username` ASC) VISIBLE,
                INDEX `room_id_idx` (`room_id` ASC) VISIBLE,
                CONSTRAINT `hotel_fk_username`
                    FOREIGN KEY (`username`)
                    REFERENCES `hotel`.`guest` (`username`)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,
                CONSTRAINT `hotel_fk_room_id`
                    FOREIGN KEY (`room_id`)
                    REFERENCES `hotel`.`room` (`room_id`)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
            );
        """
        self.execute_sql(sql)
        
    def __create_room(self) -> None:
        sql = """
        CREATE TABLE IF NOT EXISTS `room` (
            `room_id` INT NOT NULL AUTO_INCREMENT,
            `room_type` VARCHAR(45) NULL,
            `price_per_night` DECIMAL(10, 2) NULL,
            `is_available` ENUM('available', 'not_available') DEFAULT 'available',
            PRIMARY KEY (`room_id`)
            );
        """
        self.execute_sql(sql)

    def __create_transactions(self) -> None:
        sql = """
            CREATE TABLE IF NOT EXISTS `transaction` (
                `transaction_id` INT NOT NULL AUTO_INCREMENT,
                `reservation_id` INT NULL,
                `amount_paid` INT NULL,
                `payment_date` DATETIME NULL,
                `payment_method` VARCHAR(45) NULL,
                PRIMARY KEY (`transaction_id`),
                CONSTRAINT `transaction_fk_reservation_id`
                    FOREIGN KEY (`reservation_id`)
                    REFERENCES `hotel`.`reservation` (`reservation_id`)
                    ON DELETE NO ACTION
                    ON UPDATE NO ACTION);
        """
        self.execute_sql(sql)





"""



"""


