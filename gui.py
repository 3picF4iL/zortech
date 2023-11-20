import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from misc import LANG, TICKET_WINDOW_CONFIG, AutocompleteCombobox
from datetime import datetime
from json import dumps, loads


class GUIApp:
    def __init__(self, config, db):
        self.config = config
        self.database = db
        self.lang = 'pl'

        # Root
        self.root = None
        self.new_ticket_window_state = False

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
        self.root.mainloop()

    def _gui_init(self):
        self._init_root()
        self._init_main_frame()
        self._init_tree_view()
        self.display_data()
        # Print pretty-like database
        # print(dumps(self.database.tables, indent=4, sort_keys=False))

    def _init_root(self):
        root = tk.Tk()
        root.title(self.config.get("title"))
        root.geometry(self.config.get("geometry"))
        root.minsize(self.config.get("mingeometry"))
        self.root = root

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
        self.tree_view['columns'] = [
            x
            for i, x in enumerate(self.database.tables[self.active_tree_view].keys())
        ]

        self._tree_view_column_format()

        self.tree_view.bind('<Button-3>', self.on_right_click)
        self.tree_view.bind('<Button-2>', self.on_right_click)
        self.tree_view.bind('<Control-Button-1>', self.on_right_click)

        for col in self.tree_view['columns']:
            self.tree_view.heading(col, command=lambda _col=col: self._tree_sort_column(self.tree_view, _col, False))

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
        self.tree_view.delete(*self.tree_view.get_children())
        out_data = self.database.get_tickets_details()
        out_data.sort(key=lambda x: x['ticketid'], reverse=True)
        print(dumps(out_data, indent=4))
        for ticket in out_data:
            customer = ticket["customer"]["firstname"] + ' ' + ticket["customer"]["lastname"] + ' ' + ticket["customer"]["phone"]
            car = ticket['car']['brandname'].capitalize() + ' ' + ticket['car']['modelname'] + ' ' + ticket['car']['year']
            inp = ticket['ticketid'], ticket['date'], customer, car, ticket['notes']

            self.tree_view.insert('', 'end', values=inp)

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

    def change_new_ticket_button_state(self):
        if self.new_ticket_button.cget('state') == tk.DISABLED:
            self.new_ticket_button.config(state=tk.NORMAL)
        else:
            self.new_ticket_button.config(state=tk.DISABLED)

    def open_new_ticket_window(self):
        self.change_new_ticket_button_state()
        TicketWindow(lang=self.lang,
                     database=self.database,
                     parent=self)

    def quit_app(self):
        self.root.destroy()

    def _lang(self, expression):
        return LANG[self.lang].get(expression, expression)


class TicketWindow:
    def __init__(self, lang, database, parent=None):
        # Date and time with format: YYYY-MM-DD HH:MM:SS
        self.date = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
        self.window_dimension = [290, 600]
        self.window_position = [500, 200]
        self.top = None
        self.parent = parent
        self.main_frame = None

        self.lang = lang
        self.database = database
        self.database_static_values = None
        self._update_any_data()

        self.window_config = TICKET_WINDOW_CONFIG
        self.window_fields = {}
        self.window_data_values = None

        self._setup_top(
            self.window_dimension,
            self.window_position
        )
        self._setup_main_frame()
        self._build_sections()
        self._fill_data_for_test()


    # =======================================================================
    # Setup methods
    # =======================================================================
    def _setup_top(self, w_d, w_p):
        top = tk.Tk()
        top.geometry(f'{w_d[0]}x'
                     f'{w_d[1]}+'
                     f'{w_p[0]}+'
                     f'{w_p[1]}')
        top.resizable(*self.window_config['resizable'])
        top.title(
            self._lang(self.window_config['title'])
        )
        self.top = top

    def _setup_main_frame(self):
        main_frame = ttk.Frame(self.top)
        main_frame.grid(sticky='nsew', padx=10, pady=10)
        main_frame.grid_propagate(False)
        self.main_frame = main_frame
        self.top.grid_rowconfigure(0, weight=1)
        self.top.grid_columnconfigure(0, weight=1)

    def _build_sections(self):
        self._build_section('--', [
            ("date", 0), ], 0)

        self._build_section('customer', [
            ("firstname", 0),
            ("lastname", 1),
            ("phone", 2),
            ("email", 3)
        ], 1)

        self._build_section(self._lang('car'), [
            ("brand", 0),
            ("model", 1),
            ("year", 2),
            ("color", 3),
            ("vin", 4)
        ], 2)

        self._build_notes_section()
        self._build_buttons()

    def _build_section(self, title, fields, row):
        section_frame = ttk.Labelframe(self.main_frame, text=title)
        section_frame.grid(row=row, column=0, sticky='nsew', padx=5, pady=5)

        section_frame.grid_columnconfigure(0, minsize=100)
        section_frame.grid_columnconfigure(1, weight=1)

        for label_text, r in fields:
            entry = ttk.Entry(section_frame)

            if label_text == "date":
                entry.insert(0, self.date)
                entry.config(state=self.window_config['ticket_date_state'])

            # If label_text is color get color list from database
            if label_text == "color":
                entry = AutocompleteCombobox(section_frame)
                colors = [self._lang(color[1]).capitalize() for color in self.database_static_values['colors']]
                entry.set_completion_list(colors)
                entry.set("")

            if label_text == "brand":
                entry = AutocompleteCombobox(section_frame)
                brands = [brand[1].capitalize() for brand in self.database_static_values['brands']]
                entry.set_completion_list(brands)
                entry.set("")
                entry.bind("<<ComboboxSelected>>", self._on_brand_select)
                entry.bind("<Return>", self._on_brand_select)

            if label_text == "model":
                entry = AutocompleteCombobox(section_frame)
                entry.set("")

            self._collect_field(label_text, entry)
            label = ttk.Label(section_frame, text=self._lang(label_text))
            label.grid(row=r, column=0, sticky='w', padx=5, pady=5)
            entry.grid(row=r, column=1, sticky='ew', padx=5, pady=5)

        for i in range(len(fields)):
            section_frame.grid_rowconfigure(i, weight=1)

    def _build_notes_section(self):
        notes_frame = ttk.Labelframe(self.main_frame, text=self._lang('notes'))
        notes_frame.grid(row=3, column=0, sticky='w', padx=5, pady=5,)

        text = tk.Text(notes_frame, width=30, height=5, wrap='word')
        text.grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self._collect_field('notes', text)

    def _build_buttons(self):
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=4, column=0, sticky='w', padx=5, pady=5)
        button_frame.grid_columnconfigure(1, weight=1)

        ttk.Button(button_frame, text=self._lang('save'), command=self._save_ticket).\
            grid(row=0, column=0, sticky='we', padx=5, pady=5)
        ttk.Button(button_frame, text=self._lang('cancel'), command=self._close_window).\
            grid(row=0, column=1, sticky='we', padx=5, pady=5)


    def _on_brand_select(self, event=None):
        combobox = self.window_fields['model']
        selected_brand = self.window_fields['brand'].get()
        try:
            model_list = [model[1] for model in self.database_static_values['models'][selected_brand.lower()]]
        except KeyError:
            model_list = ""
        combobox.set_completion_list(model_list)

    def _collect_field(self, label_text, entry):
        self.window_fields[label_text] = entry

    # =======================================================================
    # Database methods
    # =======================================================================

    def _update_any_data(self):
        self._get_static_values_from_database()

    def _get_static_values_from_database(self):
        # Out from database e.g:
        # [
        #   (1, 'Golf', 'volkswagen'),
        #   (2, 'Polo', 'volkswagen'),
        #   (15, 'Series 1', 'bmw'),
        #   (16, 'Series 3', 'bmw'),
        #   (...)
        # ]
        model_pack = {}
        for model in self.database.fetch_models():
            if model[2] not in model_pack:
                model_pack[model[2]] = []
            # model_pack[brandname] = [[modelid, modelname], [modelid, modelname], ...] e.g.
            # model_pack['volkswagen'] = [[1, 'Golf'], [2, 'Polo']]
            model_pack[model[2]].append([model[0], model[1]])

        self.database_static_values = {
            'brands': self.database.fetch_brands(),
            'colors': self.database.fetch_colors(),
            'models': model_pack
        }

    def _fill_data_for_test(self):
        self.window_fields['firstname'].insert(0, "Test")
        self.window_fields['lastname'].insert(0, "TestSurname")
        self.window_fields['phone'].insert(0, "123456789")
        self.window_fields['email'].insert(0, "test@test.com")
        self.window_fields['vin'].insert(0, "12345678901234567")
        self.window_fields['date'].insert(0, "2021-01-01")
        self.window_fields['brand'].insert(0, "Volkswagen")
        self.window_fields['model'].insert(0, "Golf")
        self.window_fields['color'].insert(0, "Black")
        self.window_fields['notes'].insert(0.0, "Test notes")

    # def _print_static_values(self):
    #     # Print data in the JSON pretty format
    #     import json
    #     print(json.dumps(self.database_static_values, indent=4))

    def _get_data_from_entries(self):
        data = {
            'date': None,
            'customer': {
            },
            'car': {
            }
        }
        for key, value in self.window_fields.items():
            try:
                if key == "date":
                    data['date'] = value.get()
                elif key == "firstname":
                    data['customer']['firstname'] = value.get()
                elif key == "lastname":
                    data['customer']['lastname'] = value.get()
                elif key == "phone":
                    data['customer']['phone'] = value.get()
                elif key == "email":
                    data['customer']['email'] = value.get()
                elif key == "brand":
                    data['car']['brand'] = value.get()
                elif key == "model":
                    data['car']['model'] = value.get()
                elif key == "year":
                    data['car']['year'] = value.get()
                elif key == "color":
                    data['car']['color'] = value.get()
                elif key == "vin":
                    data['car']['vin'] = value.get()
                elif key == "notes":
                    data['notes'] = value.get('1.0', 'end-1c')
            except AttributeError:
                pass
        self.data = data


    # =======================================================================
    # Button events handlers
    # =======================================================================
    def _save_ticket(self):
        # Data collection
        # Data validation
        # Data conversion
        # Data saving
        self._get_data_from_entries()
        # print(self.data)
        self._prepare_data_for_saving()
        #self._validate_customer_data(self.data['customer'])
        #self._print_static_values()

    def _map_id_to_name(self, name, section):
        # Get data from self.database_static_values
        # Return id of given name
        #self._print_static_values()
        if section == 'models':
            for brand in self.database_static_values[section]:
                for model in self.database_static_values[section][brand]:
                    if model[1] == name:
                        return model[0] if model[0] else None
        if section:
            for item in self.database_static_values[section]:
                if item[1] == name.lower():
                    return item[0] if item[0] else None

    def _prepare_data_for_saving(self):
        # From data collected from entries, prepare data for saving in database
        c_id = None
        car_id = None

        ticket = {
            'date': self.data['date'],
            'customerid': None,
            'carid': None,
            'notes': self.data['notes']
        }

        car = {
            'customerid': None,
            'brandid': self._map_id_to_name(self.data['car']['brand'], 'brands'),
            'modelid': self._map_id_to_name(self.data['car']['model'], 'models'),
            'year': self.data['car']['year'],
            'colorid': self._map_id_to_name(self.data['car']['color'], 'colors'),
            'vin': self.data['car']['vin']
        }
        # Add customer to database if not exists
        c_id = self.database.check_if_customer_exists(self.data['customer'])
        print(ticket, car)

        if c_id:
            print("Customer exists")
            ticket['customerid'] = c_id[0]
            car['customerid'] = c_id[0]
        else:
            print("Customer does not exist")
            print("Creating new customer")
            ticket['customerid'] = self.database.add_item_to_table('customers', self.data['customer'])
            car['customerid'] = ticket['customerid']

        # Add Brand and Model to database if not exists
        if not car['brandid']:
            car['brandid'] = self.database.add_item_to_table('brands', self.data['car']['brand'])
        if not car['modelid']:
            data = {
                'brandid': car['brandid'],
                'modelname': self.data['car']['model']
            }
            car['modelid'] = self.database.add_item_to_table('models', data)

        if not car['colorid']:
            data = {
                'colorname': self.data['car']['color']
            }
            car['colorid'] = self.database.add_item_to_table('colors', data)

        if not car['vin']:
            car['vin'] = ""

        if not car['year']:
            car['year'] = ""

        # Add car to database if not exists
        car_id = self.database.check_if_car_exists(car)
        if car_id:
            print("Car exists")
            ticket['carid'] = car_id[0]
        else:
            print("Car does not exist")
            print("Creating new car")
            ticket['carid'] = self.database.add_item_to_table('cars', car)

        # Add ticket to database
        print("Creating new ticket")
        self.database.add_item_to_table('tickets', ticket)
        self._close_window()


    def _close_window(self):
        self.parent.change_new_ticket_button_state()
        self._get_static_values_from_database()
        self.parent.display_data()
        self.top.destroy()

    # =======================================================================
    # Helpers
    # =======================================================================

    def _lang(self, expression):
        return LANG[self.lang].get(expression, expression)
