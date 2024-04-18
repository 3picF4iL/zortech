import inspect
from database.database import Database
from misc import Entity
import sqlite3

"""
Links between the database and the application
"""


class DBProcessor(Entity):
    def __init__(self):
        super().__init__()
        self.database_name = "database/zortech_sqlite.db"
        self.database = Database(self.database_name)

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

    def fetch_all_join(self, table, columns='*', join=None, where=None, dictionary=False):
        query = f"SELECT {columns} FROM {table}"
        if join:
            query += f" JOIN {join}"
        if where:
            query += f" WHERE {where}"
        self.database.cursor.execute(query)
        results = self.database.cursor.fetchall()
        if dictionary:
            results = [{description[0]: data for description, data in
                        zip(self.database.cursor.description, result)} for result in results]

        return results

    def fetch_brands(self):
        return self.fetch_all('brands',
                              'id, name')

    def fetch_colors(self):
        return self.fetch_all('colors',
                              'id, name')

    def fetch_models(self):
        return self.fetch_all_join('models',
                                   'models.id, models.name, brand_id',
                                   'brands',
                                   'models.brand_id = brands.id'
                                   )

    def fetch_models_from_brand(self, brand_name):
        return self.fetch_all_join('models',
                                   'models.name',
                                   'brands ON models.brand_id = brands.id',
                                   f"brands.name = '{brand_name}'")

    def check_if_customer_exists(self, customer_data):
        """
        Check if customer exists in database.
        :param customer_data:
        :return:
        """
        query = "SELECT id FROM customers WHERE last_name = ? AND phone = ?"
        self.logger.debug(f"Running query: {query}")
        self.database.cursor.execute(query, (customer_data['last_name'], customer_data['phone']))
        c_id = self.database.cursor.fetchone()
        return c_id[0] if c_id else None

    def check_if_car_exists(self, car_data):
        """
        Check if car exists in database.
        :param car_data:
        :return:
        """
        query = "SELECT id FROM cars WHERE customer_id = ? AND brand_id = ?"
        self.database.cursor.execute(query, (car_data['customer_id'], car_data['brand_id']))
        c_id = self.database.cursor.fetchone()
        return c_id[0] if c_id else None

    def get_item_from_id(self, table, item_id, columns='*'):
        """
        Get item from database.
        :param item_id: ID of the item.
        :param table: Name of the table.
        :param columns: Get columns, default all
        :return:
        """
        if not item_id:
            self.logger.warning(f'Passed value to table \'{table}\' is None', exc_info=False)
            return {'name': ''}
        query = f"SELECT {columns} FROM {table} WHERE {table}.id = ?"
        self.database.cursor.execute(query, (item_id,))
        # Return data with column names as a dictionary
        return {description[0]: data for description, data in zip(self.database.cursor.description, self.database.cursor.fetchone())}

    def get_item_from_name(self, table, item_name):
        """
        Get item's ID from database by name
        :param table:
        :param item_name:
        :return:
        """
        _item_name = item_name.lower()
        query = f"""
            SELECT {table}.id FROM {table}
            WHERE {table}.name = ?
        """
        self.database.cursor.execute(query, (_item_name,))
        item_id = self.database.cursor.fetchone()
        return item_id[0] if item_id else ""

    def get_all_items(self, table, where=None):
        """
        Get all items from specified table.
        :param table: Name of the table.
        :param where: Conditions to search for.
        :return:
        """
        query = {
            'tickets': """
                SELECT tickets.id, tickets.date_creation,
                customers.first_name || ' - ' || customers.last_name || ' - ' || customers.phone, 
                brands.name || CASE WHEN models.name IS NOT NULL THEN ' - ' || models.name ELSE '' END, tickets.notes,
                tickets.status
                FROM tickets 
                LEFT JOIN customers 
                ON tickets.customer_id = customers.id 
                LEFT JOIN cars 
                ON tickets.car_id = cars.id
                LEFT JOIN brands
                ON cars.brand_id = brands.id
                LEFT JOIN models
                ON cars.model_id = models.id
            """,
            'cars': """
                SELECT cars.id, brands.name, models.name, colors.name, cars.year, cars.vin,
                customers.first_name || ' ' || customers.last_name || ' ' || customers.phone
                FROM cars
                LEFT JOIN brands
                ON cars.brand_id = brands.id
                LEFT JOIN models
                ON cars.model_id = models.id
                LEFT JOIN colors
                ON cars.color_id = colors.id
                LEFT JOIN customers
                ON cars.customer_id = customers.id
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
        values = tuple(customer_data.values()) + (customer_data['id'],)
        query = f"UPDATE customers SET {set_clause} WHERE customers.id = ?"

        self.logger.debug(f"Updating customer with ID: {customer_data['id']}...")
        self.database.cursor.execute(query, values)
        self.database.connection.commit()

    def update_car(self, car_data):
        """
        Update car data in database.
        :param car_data:  Dictionary of car data.
        :return:
        """
        set_clause = ', '.join([f"{column} = ?" for column in car_data])
        values = tuple(car_data.values()) + (car_data['id'],)
        query = f"UPDATE cars SET {set_clause} WHERE cars.id = ?"

        self.logger.debug(f"Updating car with ID: {car_data['id']}...")
        self.database.cursor.execute(query, values)
        self.database.connection.commit()

    def update_ticket(self, ticket_data):
        """
        Update ticket data in database.
        :param ticket_data:  Dictionary of ticket data.
        :return:
        """
        set_clause = ', '.join([f"{column} = ?" for column in ticket_data])
        values = tuple(ticket_data.values()) + (ticket_data['id'],)
        query = f"UPDATE tickets SET {set_clause} WHERE tickets.id = ?"

        self.logger.debug(f"Updating ticket with ID: {ticket_data['id']}...")
        self.database.cursor.execute(query, values)
        self.database.connection.commit()

    def delete_item(self, table_name, item_id):
        """
        Delete item from database.
        :param table_name: Name of the table to delete item from.
        :param item_id: ID of the item to delete.
        :return:
        """
        self.logger.warn(f"Deleting item with ID: {item_id} from {table_name}...")
        query = f"DELETE FROM {table_name} WHERE {table_name}.id = ?"
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
        self.logger.debug(f"Running query: {query} with values {values}")
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
            'colors': {c[0]: c[1].lower() for c in self.fetch_colors()},
            'models': model_pack
        }

    def map_name_to_id(self, name, section):
        # Get data from self.processor_static_values
        # Return id of given name
        # self._print_static_values()
        # Static values
        # brands: {1: 'Volkswagen', 2: 'Renault', 3: 'Peugeot' ...}
        _name = name.lower()
        self.logger.debug(f"Mapping {_name} to id from {section}...")
        if section == 'models':
            for brand in self.static_values[section]:
                for key, value in self.static_values[section][brand].items():
                    if value == _name:
                        return key if key else None
        if section:
            for key, value in self.static_values[section].items():
                if value == _name:
                    return key if key else None

    def close(self):
        self.database.close()
