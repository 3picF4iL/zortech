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

    def _create_tables(self):
        """
        Create database tables using database_schema.sql file.
        :return:
        """
        self.logger.info("* Creating tables...")
        try:
            with open("database/database_schema.sql", "r") as _schema:
                self.cursor.executescript(_schema.read())
            self.connection.commit()
            self.logger.info("* Tables created...")
        except sqlite3.Error as e:
            self.logger.exception(f"Cannot create tables, error {e}...")
            raise

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
            # Check if database exists
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            if not self.cursor.fetchall():
                self.logger.warning("Database not exists, creating tables...")
                self._create_tables()
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
