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

        self.tables = {}

        if not self.connect_to_database():
            print(f"Cannot connect to database {self.db}...")
            exit(1)
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
        except sqlite3.Error as e:
            print(f"ERROR: {e}")
            return False

    def _is_database_exists(self):
        """
        Check if database exists.
        :return:  True if database exists, False if not.
        """
        return os.path.exists(self.db)

    def _is_connection_open(self):
        """
        Check if connection to database is open.
        :return:  True if connection is open, False if not.
        """
        return self.connection is not None and self.cursor is not None

    def connect_to_database(self):
        """
        Connect to database.
        :return:  True if connection was established, False if not.
        """
        print(f"* Connecting to database {self.db}...")
        if not self._is_database_exists():
            print(f"Database {self.db} does not exist... Creating new database...")
        try:
            self.connection = sqlite3.connect(self.db)
            self.cursor = self.connection.cursor()
            print("* Connection to database initialized...")
            return True
        except sqlite3.Error as e:
            print(f"Cannot connect to database {self.db}, error {e}...")


        return False

    def close_connection(self):
        """
        Close connection to database.
        :return:
        """
        try:
            print(f"\n======\n* Closing connection to database {self.db}...")
            self.cursor.close()
            self.connection.close()
        except sqlite3.Error as e:
            print(f"ERROR: {e}")

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

    def run_command_with_output(self, command, params=()):
        """
        Run command in database and return output. Command must be passed as string.
        :param command:  Command to run.
        :param params:  Parameters for command. E.g. ("John", "Smith")
        :return:  Output of command. E.g. [("John", "Smith"), ("Adam", "Smith")]
        """
        print(f"* Running command {command}...")
        try:
            with self.connection:
                self.cursor.execute(command, params)
                return self.cursor.fetchall()
        except sqlite3.Error as e:
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

    def check_if_column_exists(self, table_name, column_name):
        """
        Check if column exists in table. Table name and column name must be passed as string.
        E.g. check_if_column_exists("users", "name")

        :param table_name:  Table name.
        :param column_name:  Column name.
        :return:  True if column exists, False if not.
        """
        if table_name in self.tables:
            return column_name in self.tables[table_name]
        return False

    def add_entry(self, table_name, columns, values):
        """
        Add entry to table. Table name, columns and values must be passed as string.
        E.g. add_entry("users", "name, age", "'John', 20")

        :param table_name:  Table name.
        :param columns:  Columns. E.g. "name, age"
        :param values:  Values. E.g. "'John', 20"
        :return:  True if entry was added, False if not.
        """
        placeholders = ', '.join(['?' for _ in values])  # Create placeholders for values (?,?,?)
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        return self.run_command(query, values)

    def edit_entry(self, table_name, column, value, where):
        """
        Edit value in table. Table name, column, value and where must be passed as string.
        E.g. edit_value("users", "name", "'John'", "id=1")

        :param table_name:  Table name.
        :param column:  Column. E.g. "name"
        :param value:  Value to set (change). E.g. "'John'"
        :param where:  Where. E.g. "id=1"
        :return:  True if value was edited, False if not.
        """
        query = f"UPDATE {table_name} SET {column}=? WHERE {where}"
        return self.run_command(query, (value,))

    def delete_entry(self, table_name, entry_id):
        """
        Delete entry from table. Table name and entry id must be passed as string.
        :param table_name:  Table name.
        :param entry_id:  Entry id.
        :return:  True if entry was deleted, False if not.
        """
        query = f"DELETE FROM {table_name} WHERE id = ?"
        return self.run_command(query, (entry_id,))

    def get_entry(self, table_name, columns, where):
        """
        Get entry from table. Table name, columns and where must be passed as string.
        E.g. get_entry("users", "name, age", "id=1")

        :param table_name:  Table name.
        :param columns:  Columns. E.g. "name, age"
        :param where:  Where. E.g. "id=1"
        :return:  Entry if it exists, None if not.
        """
        query = f"SELECT {columns} FROM {table_name} WHERE {where}"
        return self.run_command_with_output(query)

    def get_all_entries(self, table_name):
        """
        Get all entries from table. Table name and columns must be passed as string.
        E.g. get_all_entries("users", "name, age")

        :param table_name:  Table name.
        :param columns:  Columns. E.g. "name, age"
        :return:  Entries if they exist, None if not.
        """
        return self.run_command_with_output(f"SELECT * FROM {table_name}")

