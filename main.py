from gui import MainGUI
from misc import Logger

Logger.setup_logging()


class MainApplication:
    def __init__(self):
        # Create main window (layout/GUI)
        # Connect to database and fetch data
        # Use data to populate treeview
        self.gui = MainGUI()


if __name__ == '__main__':
    main = MainApplication()







