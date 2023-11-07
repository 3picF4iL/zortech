import tkinter as tk
from tkinter import messagebox, ttk, filedialog


class GUIApp:
    def __init__(self, config, db):
        self.config = config
        self.database = db
        self._database_init()

        # Root
        self.root = None
        self.root_title = None
        self.root_geometry = None
        self.root_minsize = None

        # Main Frame
        self.main_frame = None

        # Tree View
        self.tree_view = None
        self.active_tree_view = 'tickets'
        self.current_entiers_text = None

        # Top Menu
        self.top_menu = None
        self.filemenu = None
        self.menu = None
        self.menubar = None

        # Buttons
        self.new_ticket_button = None
        self.clear_button = None
        self.exit_button = None

        self.layout_config = {
            "normal_font": ('Segoe UI', 9),
            "large_font": ('Segoe UI', 12)
        }

        self._gui_init()

    def _database_init(self):
        rc = self.database.check_if_table_exists("tickets")
        if not rc:
            self.database.create_table("tickets", "id INTEGER PRIMARY KEY,"
                                                  "date TEXT, "
                                                  "name TEXT, "
                                                  "surname TEXT, "
                                                  "phone TEXT, "
                                                  "description TEXT")

    def _gui_init(self):
        self._init_values()
        self._init_root()
        self._init_main_frame()
        self._init_tree_view()
        self._init_top_menu()
        self._init_buttons()

    def _init_values(self):
        self.root_title = self.config.get("title")
        self.root_geometry = self.config.get("geometry")
        self.root_minsize = self.config.get("mingeometry")

    def _init_root(self):
        self.root = tk.Tk()
        self.root.title(self.root_title)
        self.root.geometry(self.root_geometry)
        #self.root.minsize(self.root_minsize)

    def _init_main_frame(self):
        self.main_frame = tk.Frame(self.root, padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=1)

    def _init_tree_view(self):
        self.tree_view = ttk.Treeview(self.main_frame)
        self.tree_view.pack(fill=tk.BOTH, expand=1)
        self.tree_view['columns'] = [x for x in self.database.tables[self.active_tree_view].keys()]
        self._tree_view_column_format()

        self.current_entiers_text = tk.Label(self.main_frame, text="Aktualne zgłoszenia")
        self.current_entiers_text.pack(padx=5, pady=10)

        self.tree_view.bind('<Button-3>', self.on_right_click)
        self.tree_view.bind('<Button-2>', self.on_right_click)
        self.tree_view.bind('<Control-Button-1>', self.on_right_click)

        for col in self.tree_view['columns']:
            self.tree_view.heading(col, command=lambda _col=col: self._tree_sort_column(tree, _col, False))

        self.tree_view.pack(side=tk.TOP, fill=tk.X)

    def _tree_view_column_format(self):
        for i, column in enumerate(self.tree_view['columns']):
            if i == 0:
                self.tree_view.column(column, width=0, stretch=tk.NO)
                self.tree_view.heading(column, text='', anchor=tk.CENTER)
            self.tree_view.column(column, anchor=tk.CENTER, width=80)
            self.tree_view.heading(column, text=column, anchor=tk.CENTER)

    def _tree_sort_column(self, tree, col, reverse):
        line = [(self.tree_view.set(k, col), k) for k in self.tree_view.get_children('')]
        line.sort(reverse=reverse)

        for index, (val, k) in enumerate(line):
            self.tree_view.move(k, '', index)

        self.tree_view.heading(col, command=lambda: self._tree_sort_column(tree, col, not reverse))

    def _init_top_menu(self):
        self.top_menu = tk.Frame(self.main_frame)
        self.top_menu.pack(fill=tk.X)

        self.menu = tk.Menu(self.main_frame, tearoff=0)
        self.menu.add_command(label="Usuń", command=lambda: self.delete_entry)
        self.menu.add_command(label="Edytuj", command=lambda: self.edit_entry)
        self.menubar = tk.Menu(self.main_frame, tearoff=0)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Importuj bazę danych", command=self.menu_on_open_file)
        self.filemenu.add_command(label="Wyeksportuj bazę danych", command=self.menu_on_save_file)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Wyjście", command=self.menu_on_exit)
        self.menubar.add_cascade(label="Plik", menu=self.filemenu, underline=1)
        self.root.config(menu=self.menubar)

    def _init_buttons(self):
        self.new_ticket_button = tk.Button(self.top_menu,
                                           text="Nowe Zgłoszenie",
                                           command=self.open_new_ticket_window,
                                           font=self.layout_config["large_font"])
        self.new_ticket_button.pack(side=tk.LEFT, padx=5, pady=5)
        # =======================================================================
        self.clear_button = tk.Button(self.top_menu,
                                      text="Wyczyść",
                                      command=self.create_tables,
                                      font=self.layout_config["large_font"])
        self.clear_button.pack(side=tk.LEFT, padx=5, pady=5)
        # =======================================================================
        self.exit_button = tk.Button(self.top_menu,
                                     text="X",
                                     command=self.quit_app,
                                     font=self.layout_config["large_font"])
        self.exit_button.pack(side=tk.LEFT, padx=5, pady=5)

    def on_right_click(self, event):
        try:
            self.tree_view.selection_set(tree_view.identify_row(event.y))
            self.menu.entryconfig("Usuń", command=lambda: self.delete_entry(event))
            self.menu.entryconfig("Edytuj", command=lambda: self.edit_entry(event))
            self.menu.post(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def display_data(self):
        out_data = self.database.get_all_entries(self.active_tree_view)
        out_data.sort(key=lambda x: x[0], reverse=True)

        for item in self.tree_view.get_children():
            self.tree_view.delete(item)

        print(out_data)

    def menu_on_open_file(self):
        pass

    def menu_on_save_file(self):
        pass

    def menu_on_exit(self):
        pass

    def open_new_ticket_window(self):
        pass

    def create_tables(self):
        pass

    def quit_app(self):
        pass