import inspect
from database import Database
from misc import Logger

"""
Links between the database and the application
"""


class DataProcessor:
    def __init__(self):
        self.data_base_name = "zortech_sqlite.db"
        self.database = Database(self.data_base_name)
        self.logger = Logger.get_logger(self.__class__.__name__)

        self.static_values = None

        self.get_static_values_from_database()

    def execute_query(self, query):
        """
        Execute query and fetch all results.
        :param query:
        :return:
        """
        return self.database.execute_query(query)

    def fetch_all(self, table, columns='*', where=None):
        query = f"SELECT {columns} FROM {table}"
        if where:
            query += f" WHERE {where}"
        return self.execute_query(query)

    def fetch_all_join(self, table, columns='*', join=None, where=None):
        query = f"SELECT {columns} FROM {table}"
        if join:
            query += f" JOIN {join}"
        if where:
            query += f" WHERE {where}"
        return self.execute_query(query)

    def fetch_brands(self):
        return self.fetch_all('brands',
                              'brandid, brandname')

    def fetch_colors(self):
        return self.fetch_all('colors',
                              'colorid, colorname')

    def fetch_models(self):
        return self.fetch_all_join('models', 'modelid, modelname, brandname', 'brands', 'models.brandid = brands.brandid')

    def fetch_customers(self):
        return self.fetch_all('customers',
                              'id, firstname, lastname, phone, email')

    def check_if_customer_exists(self, customer_data):
        """
        Check if customer exists in database.
        :param customer_data:
        :return:
        """
        query = "SELECT customerid FROM customers WHERE lastname = ? AND phone = ?"
        self.database.cursor.execute(query, (customer_data['lastname'], customer_data['phone']))
        return self.database.cursor.fetchone()

    def check_if_car_exists(self, car_data):
        """
        Check if car exists in database.
        :param car_data:
        :return:
        """
        query = "SELECT carid FROM cars WHERE customerid = ? AND brandid = ? AND modelid = ? AND year = ?"
        self.database.cursor.execute(query, (car_data['customerid'], car_data['brandid'], car_data['modelid'], car_data['year']))
        return self.database.cursor.fetchone()

    def update_customer(self, customer_data):
        """
        Update customer data in database.
        :param customer_data:  Dictionary of customer data.
        :return:
        """
        set_clause = ', '.join([f"{column} = ?" for column in customer_data])
        values = tuple(customer_data.values()) + (customer_data['id'],)
        query = f"UPDATE customers SET {set_clause} WHERE id = ?"
        self.database.cursor.execute(query, values)
        self.database.connection.commit()

    def add_item_to_table(self, table_name, item_data):
        """
        Add item to specified table.
        :param table_name: Name of the table to add items to.
        :param item_data: Dictionary of column names and their values to insert.
        :return: ID of the last row inserted or None if an error occurred.
        """
        columns = ', '.join(item_data.keys())
        placeholders = ', '.join(['?'] * len(item_data))
        values = tuple(item_data.values())
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        try:
            self.database.cursor.execute(query, values)
            self.database.connection.commit()
            self.logger.debug(f"Item added to {table_name}...")
            return self.database.cursor.lastrowid
        except sqlite3.Error as e:
            self.logger.exception(f"Error adding item to {table_name}: {e}")
            return None

    def get_tickets_details(self, where=None):
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
        if where:
            query += f" WHERE {where}"

        self.logger.debug(f"Executing query inside {self.__class__.__name__}.{inspect.currentframe().f_code.co_name}")
        self.database.cursor.execute(query)
        rows = self.database.cursor.fetchall()
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

    def get_static_values_from_database(self):
        # Out from database e.g:
        # [
        #   (1, 'Golf', 'volkswagen'),
        #   (2, 'Polo', 'volkswagen'),
        #   (15, 'Series 1', 'bmw'),
        #   (16, 'Series 3', 'bmw'),
        #   (...)
        # ]
        model_pack = {}
        for model in self.fetch_models():
            if model[2] not in model_pack:
                model_pack[model[2]] = []
            # model_pack[brandname] = [[modelid, modelname], [modelid, modelname], ...] e.g.
            # model_pack['volkswagen'] = [[1, 'Golf'], [2, 'Polo']]
            model_pack[model[2]].append([model[0], model[1]])

        self.static_values = {
            'brands': self.fetch_brands(),
            'colors': self.fetch_colors(),
            'models': model_pack
        }

    def map_id_to_name(self, name, section):
        # Get data from self.processor_static_values
        # Return id of given name
        # self._print_static_values()
        if section == 'models':
            for brand in self.static_values[section]:
                for model in self.static_values[section][brand]:
                    if model[1] == name:
                        return model[0] if model[0] else None
        if section:
            for item in self.static_values[section]:
                if item[1] == name.lower():
                    return item[0] if item[0] else None