import sqlite3
from misc import Entity


class Database(Entity):
    def __init__(self, db):
        super().__init__()
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

        self._connect_to_database()

        self._update_tables_description()

    def close(self):
        """
        Close database connection.
        :return:
        """
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
            self.logger.info("* Connection to database closed...")
        except sqlite3.Error as e:
            self.logger.exception(f"Cannot close connection to database {self.db}, error {e}...")
            raise

    def _update_tables_description(self):
        """
        Update tables description.
        :return:
        """
        self.logger.info("* Updating tables description...")
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        self.tables = {table[0]: {} for table in self.cursor.fetchall()}
        for table in self.tables.keys():
            self.cursor.execute(f"PRAGMA table_info({table});")
            self.tables[table] = {info[1]: info[2] for info in self.cursor.fetchall()}

    def _connect_to_database(self):
        """
        Connect to database.
        :return:  True if connection was established, False if not.
        """
        self.logger.info(f"* Connecting to database {self.db}...")
        try:
            self.connection = sqlite3.connect(self.db)
            self.cursor = self.connection.cursor()
            self.logger.info("* Connection to database initialized...")
        except sqlite3.Error as e:
            self.logger.exception(f"Cannot connect to database {self.db}, error {e}...")
            raise

    def execute_query(self, query):
        """
        Execute query and fetch results.
        :param query:
        :return:
        """
        if not query:
            self.logger.warning("Query is empty...")
            return None
        self.logger.debug(f"* Executing query: {query}")
        self.cursor.execute(query)
        return self.cursor.fetchall()
