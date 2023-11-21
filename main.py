from gui import GUIApp
from misc import APP_CONFIG, Logger

Logger.setup_logging()


class MainApplication:
    def __init__(self):
        # Create main window (layout/GUI)
        # Connect to database and fetch data
        # Use data to populate treeview
        self.app_config = APP_CONFIG
        self.gui = GUIApp(self.app_config)


main = MainApplication()







