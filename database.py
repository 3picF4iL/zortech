import sqlite3
import os


class Database:
    def __init__(self, db):
        """
        Initialize database connection and cursor.
        E.g. database = Database("database.db")
        :param db:  Path to database file.
        """
        # Variables initialization
        self.connection = None
        self.cursor = None
        self.db = db

        # Tables initialization
        # E.g. self.tables = {
        #                       "users": {
        #                          "key": "value",
        #                          (...),
        #                          "key": "value",
        #                           },
        #                       "posts": {
        #                          "key": "value",
        #                          (...),
        #                          "key": "value",
        #                           }
        #                    }
        self.tables = {}
        # Initialize methods
        if not self._init_database_exists():
            self.create_database()
        self.connect_to_database()
        self.tables_description_update()

    def tables_description_update(self):
        """
        Update tables description.
        :return:  True if tables description was updated, False if not.
        """
        print(f"\n======\n* Updating tables description...")
        try:
            tables = self.run_command_with_output("SELECT name FROM sqlite_master WHERE type='table';")
            for table in tables:
                columns = self.run_command_with_output(f"PRAGMA table_info({table[0]});")
                self.tables[table[0]] = {}
                for column in columns:
                    self.tables[table[0]][column[1]] = column[2]
            return True
        except Exception as e:
            print(f"ERROR: {e}")
            return False

    def _init_database_exists(self):
        """
        Check if database exists.
        :return:  True if database exists, False if not.
        """
        try:
            open(self.db)
            print(f"* Database {self.db} exists...")
            return True
        except Exception as e:
            print(f"* Database {self.db} does not exist...")
            return False

    def create_database(self):
        """
        Create database file.
        :return:  True if database was created, False if not.
        """
        print(f"* Creating database {self.db}...")
        try:
            open(self.db, "w")
        except Exception as e:
            print(f"ERROR: {e}")

        finally:
            # Check if finally database exists
            if os.path.exists(self.db):
                print("* Database created...")
                return True
            else:
                print("* Database not created...")
                return False

    def connect_to_database(self):
        """
        Connect to database.
        :return:  True if connection was initialized, False if not.
        """
        print(f"\n======\n* Connecting to database {self.db}...")
        try:
            if not self._connection_state():
                self.connection = sqlite3.connect(self.db)
                self.cursor = self.connection.cursor()
                print("* Connection to database initialized...")
            else:
                print("* Connection to database already initialized...")
            return True
        except Exception as e:
            print(f"Cant connect to database {self.db}, error {e}...")
            return False

    def close_connection(self):
        try:
            print(f"\n======\n* Closing connection to database {self.db}...")
            self.cursor.close()
            self.connection.close()
        except Exception as e:
            print(f"ERROR: {e}")

    def _reconnect_to_database(self):
        """
        Reconnect to database
        """
        print(f"\n======\n* Reconnecting to database {self.db}...")
        if self._connection_state():
            self.close_connection()

        self.connect_to_database()
        return self._connection_state()

    def _connection_state(self):
        """
        Check if connection and cursor are not None.
        :return:  True if connection and cursor are not None, False if not.
        """
        return self.connection is not None and self.cursor is not None

    def check_if_table_exists(self, table_name):
        """
        Check if table exists in database. Table name must be passed as string.
        E.g. check_if_table_exists("users")

        :param table_name:  Table name.
        :return:  True if table exists, False if not.
        """
        if not self._connection_state():
            self._reconnect_to_database()
        try:
            self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
            return self.cursor.fetchone() is not None
        except Exception as e:
            print(f"ERROR: {e}")
            return False

    def run_command(self, command):
        """
        Run command in database. Command must be passed as string.
        E.g. run_command("SELECT * FROM users")
             run_command("SELECT * FROM users WHERE id=%s", 1)

        :param command:  Command to run.
        :param values:  Values to pass to command.
        :param table_name:  Table name.
        :return:  True if command was run, False if not.
        """
        print(f"\n======\n* Running command {command}...")
        if not self._connection_state():
            self._reconnect_to_database()
        try:
            self.cursor.execute(command)
            self.connection.commit()
        except Exception as e:
            print(f"Error while running command {command}, error {e}...")
            return False

        print("Success")
        return True

    def run_command_with_output(self, command):
        """
        Run command in database. Command must be passed as string.
        E.g. run_command("SELECT * FROM users")
        :param command:
        :return:  List of tuples with results of command.
        """
        print(f"\n======\n* Running command {command}...")
        if not self._connection_state():
            self._reconnect_to_database()
        try:
            self.cursor.execute(command)
            print("Success")
            return self.cursor.fetchall()
        except Exception as e:
            print(f"ERROR: {e}")
            return None

    def create_table(self, table_name, columns):
        """
        Create table in database. Table name and columns must be passed as string.
        E.g. create_table("users", "id INTEGER PRIMARY KEY, name TEXT, age INTEGER")

        :param table_name:  Table name.
        :param columns:  Columns with types. E.g. "id INTEGER PRIMARY KEY, name TEXT, age INTEGER"
        :return:  True if table was created, False if not.
        """
        rc = self.run_command(f"CREATE TABLE {table_name} ({columns})")
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

    def check_if_column_exists(self, table_name, column_name):
        """
        Check if column exists in table. Table name and column name must be passed as string.
        E.g. check_if_column_exists("users", "name")

        :param table_name:  Table name.
        :param column_name:  Column name.
        :return:  True if column exists, False if not.
        """
        return self.run_command(f"SELECT {column_name} FROM {table_name}")

    def add_entry(self, table_name, columns, values):
        """
        Add entry to table. Table name, columns and values must be passed as string.
        E.g. add_entry("users", "name, age", "'John', 20")

        :param table_name:  Table name.
        :param columns:  Columns. E.g. "name, age"
        :param values:  Values. E.g. "'John', 20"
        :return:  True if entry was added, False if not.
        """

        return self.run_command(f"INSERT INTO {table_name} ({columns}) VALUES ({values})")

    def edit_value(self, table_name, column, value, where):
        """
        Edit value in table. Table name, column, value and where must be passed as string.
        E.g. edit_value("users", "name", "'John'", "id=1")

        :param table_name:  Table name.
        :param column:  Column. E.g. "name"
        :param value:  Value to set (change). E.g. "'John'"
        :param where:  Where. E.g. "id=1"
        :return:  True if value was edited, False if not.
        """

        return self.run_command(f"UPDATE {table_name} SET {column}={value} WHERE {where}")

    def delete_entry(self, table_name, where):
        """
        Delete entry from table. Table name and where must be passed as string.
        E.g. delete_entry("users", "id=1")

        :param table_name:  Table name.
        :param where:  Where. E.g. "id=1"
        :return:  True if entry was deleted, False if not.
        """
        return self.run_command(f"DELETE FROM {table_name} WHERE {where}")

    def get_entry(self, table_name, columns, where):
        """
        Get entry from table. Table name, columns and where must be passed as string.
        E.g. get_entry("users", "name, age", "id=1")

        :param table_name:  Table name.
        :param columns:  Columns. E.g. "name, age"
        :param where:  Where. E.g. "id=1"
        :return:  Entry if it exists, None if not.
        """
        return self.run_command_with_output(f"SELECT {columns} FROM {table_name} WHERE {where}")

    def get_all_entries(self, table_name):
        """
        Get all entries from table. Table name and columns must be passed as string.
        E.g. get_all_entries("users", "name, age")

        :param table_name:  Table name.
        :param columns:  Columns. E.g. "name, age"
        :return:  Entries if they exist, None if not.
        """
        return self.run_command_with_output(f"SELECT * FROM {table_name}")


class TestDataBase:
    def __init__(self, db="TestDataBase.db"):
        self.db = Database(db)

    def clear_data(self):
        self.db.run_command("DROP TABLE users")
        self.db.run_command("DROP TABLE cars")

    def prepare_data(self):
        self.clear_data()
        self.db.create_table("users", "id INTEGER PRIMARY KEY, name TEXT, age INTEGER")
        self.db.create_table("cars", "id INTEGER PRIMARY KEY, brand TEXT, model TEXT, year INTEGER")
        self.db.add_entry("users", "name, age", "'John', 20")
        self.db.add_entry("users", "name, age", "'Adam', 25")

    def run_tests(self):
        print(self.db.get_all_entries("users"))
        print(self.db.get_entry("users", "*", "id=1"))
        assert self.db.edit_value("users", "name", "'Adam'", "id=1") is True
        print(self.db.get_entry("users", "*", "id=1"))
        assert self.db.delete_entry("users", "id=1") is True
        print(self.db.get_all_entries("users"))
        assert self.db.check_if_column_exists("users", "name") is True
        assert self.db.check_if_column_exists("users", "surname") is False
        assert self.db.edit_table("users", "surname TEXT") is True
        assert self.db.check_if_column_exists("users", "surname") is True
        assert self.db.add_entry("users", "name, age, surname", "'John', 20, 'Smith'") is True
        print(self.db.get_entry("users", "*", "name='John'"))
        assert self.db.get_entry("users", "*", "name='John'") is not None
        print(self.db.get_all_entries("users"))
        assert self.db.delete_entry("users", "name='John'") is True
        print(self.db.get_all_entries("users"))
        print(self.db.tables)
        return True

    def run(self):
        self.prepare_data()
        if self.run_tests():
            print("========\nTests passed")
            if os.path.exists(self.db.db):
                self.db.close_connection()
                os.remove(self.db.db)


# if __name__ == "__main__":
#     # test = TestDataBase()
#     # test.run()
#     db = Database("service.db")
#     print(db.tables)
#     print(db.get_all_entries("tickets"))
