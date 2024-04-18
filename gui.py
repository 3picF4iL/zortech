import tkinter as tk
from tkinter import ttk
from gui_elements import (
    TreeViewSelector,
    NewTicketWindow,
    EditTicketWindow,
    EditCustomerWindow)
from misc import Entity, popup
from database.database_model import DBProcessor


class MainGUI(Entity):
    def __init__(self, database):
        super().__init__()
        self.database = database
        # Create main window (layout/GUI)
        self.root = None
        self.tabs = None
        self.active_tab = 'tickets'
        self.tree_views = {}

        self._init_gui()

    def _init_gui(self):
        self.logger.debug("* Initializing GUI...")
        try:
            self._init_main_frame()
            self._init_top_dropdown_menu()
            self._init_tree_views()
            self._init_buttons()
        except Exception as e:
            self._pop_error('error_loading_gui', str(e))
        self.root.mainloop()

    def _init_root(self):
        self.logger.debug("\tInitializing root...")
        root = tk.Tk()
        root.title(self.app_config.get("title"))
        root.geometry(self.app_config.get("geometry"))
        root.minsize(self.app_config.get("mingeometry"))
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=1)
        self.root = root

    def _init_main_frame(self):
        self._init_root()
        self.logger.debug("\tInitializing main frame...")
        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=1, column=0, sticky='nsew')

    def _init_top_dropdown_menu(self):
        self.logger.debug("\tInitializing top dropdown menu...")
        top_menu = tk.Frame(self.main_frame)
        top_menu.grid(row=0, column=0, sticky='ew')

        menubar = tk.Menu(self.main_frame, tearoff=0)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label=self._lang('import_db'), command=self.menu_on_open_file)
        filemenu.add_command(label=self._lang('export_db'), command=self.menu_on_save_file)
        filemenu.add_separator()
        filemenu.add_command(label=self._lang('settings'), command=self.menu_on_settings)
        filemenu.add_separator()
        filemenu.add_command(label=self._lang('exit'), command=self.menu_on_exit)

        menubar.add_cascade(label=self._lang('file'), menu=filemenu, underline=1)

        self.root.config(menu=menubar)

    def _init_buttons(self):
        self.logger.debug("\tInitializing buttons...")
        new_ticket_button = tk.Button(self.main_frame,
                                      text=self._lang('new_ticket'),
                                      command=self.open_new_ticket_window,
                                      font=self.app_config["layout_config"]["large_font"])
        new_ticket_button.grid(row=0, column=0, sticky='ew', padx=5, pady=5)

        exit_button = tk.Button(self.main_frame,
                                text=self._lang('exit'),
                                command=self.quit_app,
                                font=self.app_config["layout_config"]["large_font"])
        exit_button.grid(row=2, column=0, sticky='ew', padx=5, pady=5)

    def _init_tree_views(self):
        self.logger.debug("\tInitializing tree views...")
        notebook_tabs = {
            'tickets': ['ID', 'date', 'customer', 'car', 'notes'],
            'customers': ['ID', 'customer_first_name', 'customer_last_name', 'email', 'phone'],
            'cars': ['ID', 'brand_name', 'model_name', 'color_name', 'year', 'vin', 'customer'],
        }
        notebook = ttk.Notebook(self.main_frame)
        notebook.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        for tab in notebook_tabs.keys():
            tab_frame = ttk.Frame(notebook)
            notebook.add(tab_frame, text=self._lang(tab))
            tv = TreeViewSelector(tab_frame, notebook_tabs[tab], tab, self)
            self.tree_views[tab] = tv.treeview

        self.logger.debug("\t\tTree views: %s", self.tree_views)
        self.tabs = notebook
        self._init_active_tab()

    def _init_active_tab(self):
        self.logger.debug("\tInitializing active tab...")
        self.tabs.select(0)

    def delete_entry(self):
        pass

    def menu_on_open_file(self):
        popup('info', self._lang('info'), self._lang('not_implemented'))

    def menu_on_save_file(self):
        popup('info', self._lang('info'), self._lang('not_implemented'))

    def menu_on_settings(self):
        popup('info', self._lang('info'), self._lang('not_implemented'))

    def menu_on_exit(self):
        self.quit_app()

    def open_new_ticket_window(self):
        self.logger.info("* Opening new ticket window...")
        NewTicketWindow(self)

    def update_treeview(self, tab):
        self.logger.info("* Updating tree view...")
        self.tree_views[tab].populate_treeview()

    def update_treeviews(self):
        self.logger.info("* Updating tree views...")
        for tw in self.tree_views.values():
            tw.populate_treeview()

    def _pop_error(self, msg, e):
        self.logger.exception(msg, exc_info=True)
        popup('error', self._lang('error'), self._lang(msg) + '\n' + str(e))
        self.instant_quit()

    def instant_quit(self):
        self.logger.info("* Instant quitting app...")
        self.root.destroy()

    def quit_app(self):
        rc = popup('askyesno', self._lang('exit'), self._lang('ask_exit'))
        if rc:
            self.database.close()
            self.logger.info("* Quitting app...")
            self.root.destroy()
