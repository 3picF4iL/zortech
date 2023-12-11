import inspect
from database import Database
from misc import Entity
import sqlite3

"""
Links between the database and the application
"""


class DBProcessor(Entity):
    def __init__(self):
        super().__init__()
        self.database_name = "zortech_sqlite.db"
        self.database = Database(self.database_name)

        self.static_values = None

        self.get_static_values_from_database()
        self.logger.debug(f"Static values: {self.static_values}")

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
        c_id = self.database.cursor.fetchone()
        return c_id[0] if c_id else None

    def check_if_car_exists(self, car_data):
        """
        Check if car exists in database.
        :param car_data:
        :return:
        """
        query = "SELECT carid FROM cars WHERE customerid = ? AND brandid = ? AND year = ?"
        self.database.cursor.execute(query, (car_data['customerid'], car_data['brandid'], car_data['year']))
        c_id = self.database.cursor.fetchone()
        return c_id[0] if c_id else None

    def get_item_id(self, table, conditions):
        """
        Get item ID from database.
        :param conditions:  Conditions to search for.
        :param table: Name of the table.
        :return:
        """
        self.logger.debug(f"get_item_id({table}, {conditions})")
        query = f"SELECT {table[:-1]}id FROM {table} WHERE ?"
        self.database.cursor.execute(query, (conditions,))
        return self.database.cursor.fetchone()

    def get_item_from_id(self, table, item_id):
        """
        Get item from database.
        :param item_id: ID of the item.
        :param table: Name of the table.
        :return:
        """
        query = f"SELECT * FROM {table} WHERE {table[:-1]}id = ?"
        self.database.cursor.execute(query, (item_id,))
        return self.database.cursor.fetchone()

    def get_customer_cars_ids(self, customer_id):
        """
        Get customer cars ID from database.
        :param customer_id: ID of the customer.
        :return:
        """
        query = "SELECT carid FROM cars WHERE customerid = ?"
        self.database.cursor.execute(query, (customer_id,))
        return self.database.cursor.fetchall()

    def get_all_items(self, table, where=None):
        """
        Get all items from specified table.
        :param table: Name of the table.
        :param where: Conditions to search for.
        :return:
        """
        query = {
            'tickets': """
                SELECT tickets.ticketid, tickets.date,
                customers.firstname || ' - ' || customers.lastname || ' - ' || customers.phone, 
                brands.brandname || ' - ' || models.modelname, tickets.notes 
                FROM tickets 
                LEFT JOIN customers 
                ON tickets.customerid = customers.customerid 
                LEFT JOIN cars 
                ON tickets.carid = cars.carid
                LEFT JOIN brands
                ON cars.brandid = brands.brandid
                LEFT JOIN models
                ON cars.modelid = models.modelid
            """,
            'cars': """
                SELECT cars.carid, brands.brandname, models.modelname, colors.colorname, cars.year, cars.vin,
                customers.firstname || ' ' || customers.lastname || ' ' || customers.phone
                FROM cars
                LEFT JOIN brands
                ON cars.brandid = brands.brandid
                LEFT JOIN models
                ON cars.modelid = models.modelid
                LEFT JOIN colors
                ON cars.colorid = colors.colorid
                LEFT JOIN customers
                ON cars.customerid = customers.customerid
            """,
            'customers': f"SELECT * FROM {table}",
        }

        if where:
            query[table] += f" WHERE {where}"
        self.database.cursor.execute(query[table])
        return self.database.cursor.fetchall()

    def update_customer(self, customer_data):
        """
        Update customer data in database.
        :param customer_data:  Dictionary of customer data.
        :return:
        """
        set_clause = ', '.join([f"{column} = ?" for column in customer_data])
        values = tuple(customer_data.values()) + (customer_data['customerid'],)
        query = f"UPDATE customers SET {set_clause} WHERE customerid = ?"

        self.logger.debug(f"Updating customer with ID: {customer_data['customerid']}...")
        self.database.cursor.execute(query, values)
        self.database.connection.commit()

    def update_car(self, car_data):
        """
        Update car data in database.
        :param car_data:  Dictionary of car data.
        :return:
        """
        set_clause = ', '.join([f"{column} = ?" for column in car_data])
        values = tuple(car_data.values()) + (car_data['carid'],)
        query = f"UPDATE cars SET {set_clause} WHERE carid = ?"

        self.logger.debug(f"Updating car with ID: {car_data['carid']}...")
        self.database.cursor.execute(query, values)
        self.database.connection.commit()

    def update_ticket(self, ticket_data):
        """
        Update ticket data in database.
        :param ticket_data:  Dictionary of ticket data.
        :return:
        """
        set_clause = ', '.join([f"{column} = ?" for column in ticket_data])
        values = tuple(ticket_data.values()) + (ticket_data['ticketid'],)
        query = f"UPDATE tickets SET {set_clause} WHERE ticketid = ?"

        self.logger.debug(f"Updating ticket with ID: {ticket_data['ticketid']}...")
        self.database.cursor.execute(query, values)
        self.database.connection.commit()

    def get_columns_from_table(self, table_name):
        """
        Get columns from table.
        :param table_name: Name of the table to get columns from.
        :return: List of columns.
        """
        query = f"PRAGMA table_info({table_name})"
        self.database.cursor.execute(query)
        return [column[1] for column in self.database.cursor.fetchall()]

    def delete_ticket(self, ticket_id):
        """
        Delete ticket from database.
        :param ticket_id: ID of the ticket to delete.
        :return:
        """
        self.logger.warn(f"Deleting ticket with ID: {ticket_id}...")
        query = "DELETE FROM tickets WHERE ticketid = ?"
        self.database.cursor.execute(query, (ticket_id,))
        self.database.connection.commit()

    def delete_item(self, table_name, item_id):
        """
        Delete item from database.
        :param table_name: Name of the table to delete item from.
        :param item_id: ID of the item to delete.
        :return:
        """
        self.logger.warn(f"Deleting item with ID: {item_id} from {table_name}...")
        query = f"DELETE FROM {table_name} WHERE {table_name[:-1]}id = ?"
        self.database.cursor.execute(query, (item_id,))
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
        fetched_models = self.fetch_models()
        for model in fetched_models:
            # Get names list of the model depending on brand
            model_pack[model[2]] = {m[0]: m[1] for m in fetched_models if m[2] == model[2]}

        self.static_values = {
            'brands': {b[0]: b[1] for b in self.fetch_brands()},
            'colors': {c[0]: self._lang(c[1]).lower() for c in self.fetch_colors()},
            'models': model_pack
        }

    def map_id_to_name(self, name, section):
        # Get data from self.processor_static_values
        # Return id of given name
        # self._print_static_values()
        self.logger.debug(f"Mapping {name} to id from {section}...")
        if section == 'models':
            for brand in self.static_values[section]:
                for model in self.static_values[section][brand]:
                    if model[1] == name:
                        return model[0] if model[0] else None
        if section:
            for item in self.static_values[section].values():
                if item == name:
                    return item if item else None

    def map_name_to_id(self, name, section):
        # Get data from self.processor_static_values
        # Return id of given name
        # self._print_static_values()
        # Static values
        # brands: {1: 'Volkswagen', 2: 'Renault', 3: 'Peugeot' ...}
        self.logger.debug(f"Mapping {name} to id from {section}...")
        if section == 'models':
            for brand in self.static_values[section]:
                for key, value in self.static_values[section][brand].items():
                    if value == name:
                        return key if key else None
        if section:
            for key, value in self.static_values[section].items():
                if value == name:
                    return key if key else None

    def close(self):
        self.database.close()
