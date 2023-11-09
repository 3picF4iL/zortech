import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from misc import LANG
from datetime import datetime


class GUIApp:
    def __init__(self, config, db):
        self.config = config
        self.database = db
        self._database_init()
        self.lang = 'pl'

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
        self.current_entries_text = None

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
                                                  "car TEXT, "
                                                  "vin TEXT, "
                                                  "notes TEXT")

    def _gui_init(self):
        self._init_values()
        self._init_root()
        self._init_main_frame()
        self._init_tree_view()
        self.display_data()

    def _init_values(self):
        self.root_title = self.config.get("title")
        self.root_geometry = self.config.get("geometry")
        self.root_minsize = self.config.get("mingeometry")

    def _init_root(self):
        self.root = tk.Tk()
        self.root.title(self.root_title)
        self.root.geometry(self.root_geometry)

    def _init_main_frame(self):
        self.main_frame = tk.Frame(self.root, padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=1)
        self._init_top_menu()
        self._init_buttons()

        self.current_entries_text = tk.Label(self.main_frame, text=self._lang('current_entries'))
        self.current_entries_text.pack(padx=5, pady=(100, 0))

    def _init_tree_view(self):
        self.tree_view = ttk.Treeview(self.main_frame)
        self.tree_view.pack(fill=tk.BOTH, expand=1)
        self.tree_view['columns'] = [x for x in self.database.tables[self.active_tree_view].keys() if x != 'id']

        self._tree_view_column_format()

        self.tree_view.bind('<Button-3>', self.on_right_click)
        self.tree_view.bind('<Button-2>', self.on_right_click)
        self.tree_view.bind('<Control-Button-1>', self.on_right_click)

        for col in self.tree_view['columns']:
            self.tree_view.heading(col, command=lambda _col=col: self._tree_sort_column(tree, _col, False))

        self.tree_view.pack(side=tk.TOP, fill=tk.X, pady=(0, 50))

    def _tree_view_column_format(self):
        self.tree_view.column('#0', width=0, stretch=tk.NO)
        for i, column in enumerate(self.tree_view['columns']):
            self.tree_view.column(column, width=30, anchor=tk.CENTER)
            self.tree_view.heading(column, text=self._lang(column), anchor=tk.CENTER)

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
        self.menu.add_command(label=self._lang('delete'), command=lambda: self.delete_entry)
        self.menu.add_command(label=self._lang('edit'), command=lambda: self.edit_entry)

        self.menubar = tk.Menu(self.main_frame, tearoff=0)

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label=self._lang('import_db'), command=self.menu_on_open_file)
        self.filemenu.add_command(label=self._lang('export_db'), command=self.menu_on_save_file)
        self.filemenu.add_separator()
        self.filemenu.add_command(label=self._lang('exit'), command=self.menu_on_exit)

        self.menubar.add_cascade(label=self._lang('file'), menu=self.filemenu, underline=1)

        self.root.config(menu=self.menubar)

    def _init_buttons(self):
        separator = ttk.Separator(self.top_menu, orient='horizontal')
        separator.pack(fill='x', pady=(0, 5))
        self.new_ticket_button = tk.Button(self.top_menu,
                                           text=self._lang('new_ticket'),
                                           command=self.open_new_ticket_window,
                                           font=self.layout_config["large_font"])
        self.new_ticket_button.pack(side=tk.LEFT, padx=(20, 5), pady=5)
        # =======================================================================
        self.exit_button = tk.Button(self.top_menu,
                                     text=self._lang('exit'),
                                     command=self.quit_app,
                                     font=self.layout_config["large_font"])
        self.exit_button.pack(side=tk.RIGHT, padx=(5, 20), pady=5)

    def on_right_click(self, event):
        try:
            self.tree_view.selection_set(self.tree_view.identify_row(event.y))
            self.menu.entryconfig(self._lang('delete'), command=lambda: self.delete_entry(event))
            self.menu.entryconfig(self._lang('edit'), command=lambda: self.edit_entry(event))
            self.menu.post(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def display_data(self):
        out_data = self.database.get_all_entries(self.active_tree_view)
        print(out_data)
        out_data.sort(key=lambda x: x[0], reverse=True)

        for item in self.tree_view.get_children():
            self.tree_view.delete(item)

        for item in out_data:
            self.tree_view.insert('', 'end', values=item)

    def delete_entry(self, event):
        selected_item = self.tree_view.identify_row(event.y)
        if selected_item:
            self.database.delete_entry(self.active_tree_view, self.tree_view.item(selected_item)['values'][0])
            self.display_data()

    def menu_on_open_file(self):
        pass

    def menu_on_save_file(self):
        pass

    def menu_on_exit(self):
        pass

    def open_new_ticket_window(self):
        TicketWindow(lang=self.lang,
                     database=self.database,
                     table=self.active_tree_view,
                     parent=self)

    def edit_entry(self, event):
        selected_item = self.tree_view.identify_row(event.y)
        if selected_item:
            EditTicketWindow(lang=self.lang,
                            database=self.database,
                            table=self.active_tree_view,
                            parent=self,
                            data=self.tree_view.item(selected_item)['values'])
    def create_tables(self):
        pass

    def quit_app(self):
        self.root.destroy()

    def _lang(self, expression):
        return LANG[self.lang].get(expression, 'NULL')


class TicketWindow:
    def __init__(self, lang, database, table, parent):
        self.date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.lang = lang
        self.database = database
        self.table = database.tables[table]
        self.parent = parent
        self.data = None

        self.new_ticket_window = tk.Toplevel()
        self.new_ticket_window.geometry("600x300+1000+50")
        self.new_ticket_window.wm_resizable(True, True)
        self.new_ticket_window.title(self._lang('new_ticket'))
        self.main_frame = None
        self.frame_left = None

        self.frame_left_label = None
        self.frame_left_entry = None
        self.frame_right = None
        self.frame_right_label = None
        self.frame_right_entry = None
        self.frame_bottom = None
        self.frame_bottom_label = None
        self.frame_bottom_entry = None

        self.create_layout()

        self.data = self.prepare_table_data()

        self.display_buttons()

        self.new_ticket_window.mainloop()

    def create_layout(self):
        self.main_frame = tk.Frame(self.new_ticket_window)
        self.main_frame.pack(fill="both", padx=10, pady=5, expand=False)

        self.frame_left = tk.Frame(self.main_frame)
        self.frame_left.pack(side="left", padx=5, fill="both", expand=False)

        self.frame_left_label = tk.Frame(self.frame_left)
        self.frame_left_label.pack(side="left", fill="both", expand=False)
        self.frame_left_entry = tk.Frame(self.frame_left)
        self.frame_left_entry.pack(side="right", fill="both", expand=False)

        self.frame_right = tk.Frame(self.main_frame)
        self.frame_right.pack(side="right", padx=5, fill="both", expand=False)

        self.frame_right_label = tk.Frame(self.frame_right)
        self.frame_right_label.pack(side="left", fill="both", expand=False)
        self.frame_right_entry = tk.Frame(self.frame_right)
        self.frame_right_entry.pack(side="right", fill="both", expand=False)

        self.frame_bottom = tk.Frame(self.new_ticket_window)
        self.frame_bottom.pack(pady=10)

    def display_buttons(self):
        self.save_button = tk.Button(self.frame_bottom, text=self._lang('save'),
                                     command=lambda: self.save_ticket(self.new_ticket_window, self.data))
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.cancel_button = tk.Button(self.frame_bottom, text=self._lang('cancel'),
                                       command=self.new_ticket_window.destroy)
        self.cancel_button.pack(side=tk.LEFT, padx=5, pady=5)

    def prepare_table_data(self):
        labels = []
        entries = []
        keys = []

        for key, value in self.table.items():
            if key == 'id':
                continue
            keys.append(key)

            label_side, entry_side = self.frame_left_label, self.frame_left_entry
            entry_type = tk.Entry
            if key == 'notes':
                entry_type = tk.Text
                label_side, entry_side = self.frame_right_label, self.frame_right_entry

            label = tk.Label(label_side, text=self._lang(key))
            entry = entry_type(entry_side)

            if key == 'date':
                entry.insert(0, self.date)
                entry.config(state='readonly')
            if key == 'notes':
                entry.config(height=10)

            labels.append(label)
            entries.append(entry)

        for label, entry in zip(labels, entries):
            label.pack(padx=5, pady=5)
            entry.pack(padx=5, pady=5)

        return dict(zip(keys, entries))

    def convert_data_for_db_command(self, data, _type):
        # TODO: add support for other types of commands
        # TODO: add support for other types of tables
        types = {
            'insert': 'INSERT INTO tickets ({KEYS}) VALUES ({VALUES})',
            'update': 'UPDATE tickets SET {VALUES} WHERE id={ID}',
            'delete': 'DELETE FROM tickets WHERE id={ID}'
        }

        if _type == 'insert':
            keys = ', '.join(data.keys())
            # This shitty hack is needed because tk.Entry and tk.Text have different methods for getting data
            values = ', '.join([
                f'"{value.get()}"' if isinstance(value, tk.Entry)
                else f'"{value.get("1.0", "end-1c").strip()}"'
                for value in data.values()
            ])
            return types[_type].format(KEYS=keys, VALUES=values)

        if _type == 'update':
            values = ', '.join([f'{key}="{value.get()}"' for key, value in data.items()])
            return types[_type].format(VALUES=values, ID=self.data['id'].get())

        if _type == 'delete':
            return types[_type].format(ID=self.data['id'].get())

    def save_ticket(self, w, data, _type='insert'):
        query = self.convert_data_for_db_command(data, _type)
        self.database.run_command(query)
        self.parent.display_data()
        w.destroy()
        # FIXME: Show popups
        #show_popup("info", "Zgłoszenie", "Zgłoszenie zostało zapisane")

    # def delete_ticket_entry(self, event):
    #     selected_item = tree.identify_row(event.y)
    #     if selected_item:
    #         tree.delete(selected_item)
    #         query = self.convert_data_for_db_command(selected_item, 'delete')
    #         self.database.run_command(query)
    #     # FIXME: Show popups

    def _lang(self, expression):
        return LANG[self.lang].get(expression, 'NULL')


# class EditTicketWindow(TicketWindow):
#     def __init__(self, lang, database, parent, table, data):
#         super().__init__(lang, database, parent, table)
#         self.new_ticket_window.title(self._lang('edit_ticket'))
#         self.fill_data(data)
#         self.save_button.config(command=lambda: self.save_ticket(self.new_ticket_window, self.data, 'update'))
#
#     def fill_data(self, data):
#         for key, value in self.table.items():
#             if key == 'id':
#                 continue
#             if key == 'date':
#                 data[key].config(state='normal')
#                 data[key].insert(0, value)
#                 data[key].config(state='readonly')
#             elif key == 'notes':
#                 data[key].insert('1.0', value)
#             else:
#                 data[key].insert(0, value)
