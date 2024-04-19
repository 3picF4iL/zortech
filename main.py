from gui import MainGUI
from database.database_model import DBProcessor
from misc import Logger

Logger.setup_logging()


class ZortechApp:
    def __init__(self):
        # Create main window (layout/GUI)
        # Connect to database and fetch data
        # Use data to populate treeview
        self.database = DBProcessor()
        self.gui = MainGUI(self.database)
        pass


if __name__ == '__main__':
    main = ZortechApp()
