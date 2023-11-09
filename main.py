from datetime import datetime
from database import Database
from gui import GUIApp
from misc import APP_CONFIG


class MainApplication:
    def __init__(self):
        # Create main window (layout/GUI)
        # Connect to database and fetch data
        # Use data to populate treeview
        self.app_config = APP_CONFIG
        self.data_base_name = "zortech_sqlite.db"
        self.db = Database(self.data_base_name)

        self.gui = GUIApp(self.app_config, self.db)


main = MainApplication()






