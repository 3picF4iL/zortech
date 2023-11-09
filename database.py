import sqlite3
import os
from misc import LANG


class Database:
    def __init__(self, db):
        """
        Initialize database connection and cursor.
        E.g. database = Database("database.db")
        :param db:  Path to database file.
        """
        # Variables initialization
        self.db = db
        self.connection = None
        self.cursor = None

        self.lang = 'en'

        self.tables = {}

        if not self._connect_to_database():
            print(f"Cannot connect to database {self.db}...")
            exit(1)
        self._update_tables_description()

    def __del__(self):
        self._close_connection()

    def _update_tables_description(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        self.tables = {table[0]: {} for table in self.cursor.fetchall()}
        for table in self.tables.keys():
            self.cursor.execute(f"PRAGMA table_info({table});")
            self.tables[table] = {info[1]: info[2] for info in self.cursor.fetchall()}

    def _create_placeholder(self, values):
        """
        Create placeholder for SQL command. E.g. ("John", "Smith") -> (?, ?)
        :param values:  Values to create placeholder.
        :return:  Placeholder. E.g. ?, ?, ?
        """
        return ', '.join(['?' for _ in values])  # Create placeholders for values (?,?,?)

    def _connect_to_database(self):
        """
        Connect to database.
        :return:  True if connection was established, False if not.
        """
        print(f"* Connecting to database {self.db}...")
        try:
            self.connection = sqlite3.connect(self.db)
            self.cursor = self.connection.cursor()
            print("* Connection to database initialized...")
            return True
        except sqlite3.Error as e:
            print(f"Cannot connect to database {self.db}, error {e}...")

        return False

    def _close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

        print("* Connection to database closed...")

    def check_if_table_exists(self, table_name):
        """
        Check if table exists in database. Table name must be passed as string.
        E.g. check_if_table_exists("users")

        :param table_name:  Table name.
        :return:  True if table exists, False if not.
        """
        return table_name in self.tables.keys()

    def run_command(self, command, params=()):
        """
        Run command in database. Command must be passed as string.
        :param command:  Command to run. E.g. "INSERT INTO users VALUES (?, ?)"
        :param params:  Parameters for command. E.g. ("John", "Smith")
        :return:  True if command was run, False if not.
        """
        print(f"* Running command {command}...")
        try:
            with self.connection:
                self.cursor.execute(command, params)
            print("Success")
            return True
        except sqlite3.Error as e:
            print(f"Error while running command {command}, error {e}...")
            return False

    def fetch_all(self, table, columns='*', where=None):
        query = f"SELECT {columns} FROM {table}"
        if where:
            query += f" WHERE {where}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def fetch_all_join(self, table, columns='*', join=None, where=None):
        query = f"SELECT {columns} FROM {table}"
        if join:
            query += f" JOIN {join}"
        if where:
            query += f" WHERE {where}"
        self.cursor.execute(query)
        out = self.cursor.fetchall()
        return out

    def fetch_brands(self):
        return self.fetch_all('brands', 'brandid, brandname')

    def fetch_colors(self):
        return self.fetch_all('colors', 'colorid, colorname')

    def fetch_models(self):
        return self.fetch_all_join('models', 'modelid, modelname, brandname', 'brands', 'models.brandid = brands.brandid')

    def fetch_customers(self):
        return self.fetch_all('customers', 'id, firstname, lastname, phone, email')

    def check_if_customer_exists(self, customer_data):
        query = "SELECT customerid FROM customers WHERE lastname = ? AND phone = ?"
        self.cursor.execute(query, (customer_data['lastname'], customer_data['phone']))
        return self.cursor.fetchone()

    def check_if_car_exists(self, car_data):
        query = "SELECT carid FROM cars WHERE customerid = ? AND brandid = ? AND modelid = ? AND year = ?"
        self.cursor.execute(query, (car_data['customerid'], car_data['brandid'], car_data['modelid'], car_data['year']))
        return self.cursor.fetchone()

    def update_customer(self, customer_data):
        set_clause = ', '.join([f"{column} = ?" for column in customer_data])
        values = tuple(customer_data.values()) + (customer_data['id'],)
        query = f"UPDATE customers SET {set_clause} WHERE id = ?"
        self.cursor.execute(query, values)
        self.connection.commit()

    def add_customer(self, customer_data):
        columns = ', '.join(customer_data.keys())
        placeholders = ', '.join(['?'] * len(customer_data))
        values = tuple(customer_data.values())
        query = f"INSERT INTO customers ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, values)
        self.connection.commit()
        return self.cursor.lastrowid

    def add_brand(self, brand_data):
        columns = ', '.join(brand_data.keys())
        placeholders = ', '.join(['?'] * len(brand_data))
        values = tuple(brand_data.values())
        query = f"INSERT INTO brands ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, values)
        self.connection.commit()
        return self.cursor.lastrowid

    def add_model(self, model_data):
        columns = ', '.join(model_data.keys())
        placeholders = ', '.join(['?'] * len(model_data))
        values = tuple(model_data.values())
        query = f"INSERT INTO models ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, values)
        self.connection.commit()
        return self.cursor.lastrowid

    def add_car(self, car_data):
        columns = ', '.join(car_data.keys())
        placeholders = ', '.join(['?'] * len(car_data))
        values = tuple(car_data.values())
        query = f"INSERT INTO cars ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, values)
        self.connection.commit()
        return self.cursor.lastrowid

    def add_color(self, color):
        query = "INSERT INTO colors (colorname) VALUES (?)"
        # Translate color name to english and lowercase
        color = self._lang(color).lower()
        self.cursor.execute(query, (color,))
        return self.cursor.lastrowid

    def add_ticket(self, ticket_data):
        columns = ', '.join(ticket_data.keys())
        placeholders = ', '.join(['?'] * len(ticket_data))
        values = tuple(ticket_data.values())
        query = f"INSERT INTO tickets ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, values)
        self.connection.commit()
        return self.cursor.lastrowid

    def get_ticket_data(self, ticket_id):
        query = "SELECT * FROM tickets WHERE ticketid = ?"
        self.cursor.execute(query, (ticket_id,))
        return self.cursor.fetchone()

    def get_tickets_details(self):
        query = """
        SELECT 
            t.ticketid AS TicketID,
            t.date AS TicketDate,
            cu.firstname AS CustomerFirstName,
            cu.lastname AS CustomerLastName,
            cu.phone AS CustomerPhone,
            b.brandname AS BrandName,
            m.modelname AS ModelName,
            ca.year AS CarYear,
            t.notes AS TicketNotes
        FROM 
            tickets AS t
        JOIN 
            customers AS cu ON t.customerid = cu.customerid
        JOIN 
            cars AS ca ON t.carid = ca.carid
        JOIN 
            brands AS b ON ca.brandid = b.brandid
        JOIN 
            models AS m ON ca.modelid = m.modelid;
        """

        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        print(rows)
        ticket_details = []
        for row in rows:
            details = {
                    'ticketid': row[0],
                    'date': row[1],
                    'customer': {
                        'firstname': row[2], 'lastname': row[3], 'phone': row[4]
                    },
                    'car': {
                        'brandname': row[5], 'modelname': row[6], 'year': row[7]
                    },
                    'notes': row[8]
            }
            ticket_details.append(details)
        return ticket_details

    def _lang(self, expression):
        return LANG[self.lang].get(expression, expression)


class AddidionalFunctions:
    def create_table(self, table_name, columns):
        """
        Create table in database. Table name and columns must be passed as string.
        E.g. create_table("users", "id INTEGER PRIMARY KEY, name TEXT, age INTEGER")

        :param table_name:  Table name.
        :param columns:  Columns with types. E.g. "id INTEGER PRIMARY KEY, name TEXT, age INTEGER"
        :return:  True if table was created, False if not.
        """
        placeholder = ", ".join(["?"] * len(columns.split(",")))
        rc = self.run_command(f"INSERT INTO {table_name} VALUES ({placeholder})", columns.split(","))
        self.tables_description_update()
        return rc

    def edit_table(self, table_name, columns):
        """
        Edit table in database. Table name and columns must be passed as string.
        E.g. edit_table("users", "id INTEGER PRIMARY KEY, name TEXT, age INTEGER")

        :param table_name:  Table name.
        :param columns:  Columns with types. E.g. "id INTEGER PRIMARY KEY, name TEXT, age INTEGER"
        :return:  True if table was edited, False if not.
        """

        rc = self.run_command(f"ALTER TABLE {table_name} ADD {columns}")
        self.tables_description_update()
        return rc

    def delete_table(self, table_name):
        """
        Delete table in database. Table name must be passed as string.
        E.g. delete_table("users")

        :param table_name:  Table name.
        :return:  True if table was deleted, False if not.
        """
        rc = self.run_command(f"DROP TABLE {table_name}")
        self.tables_description_update()
        return rc
