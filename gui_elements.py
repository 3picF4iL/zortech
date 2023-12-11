from misc import (
    Entity,
    WINDOWS_SETTINGS,
    Logger,
    popup)
import datetime
import tkinter as tk
import re
from tkinter import ttk


class Treeview(Entity):
    def __init__(self, tab, columns, name, parent):
        super().__init__()
        self.tab = tab
        self.columns = columns
        self.name = name
        self.parent = parent
        self.database = parent.database
        self._init_treeview()
        self.populate_treeview()

    def _init_treeview(self):
        self.logger.debug("\tInitializing treeview...")
        self.treeview = ttk.Treeview(self.tab, columns=self.columns, show='headings')
        self.treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._init_treeview_columns()
        self._init_treeview_scrollbar()
        self._init_treeview_menu()

    def _init_treeview_columns(self):
        self.logger.debug("\tInitializing treeview columns...")

        for column in self.columns:
            # TODO: get width from config for ID column and set it to -100 approx
            # width = TICKET_WINDOW_LAYOUT.get('treeview', {}).get('width', 30)
            if column.lower() == 'id':
                self.treeview.column(column, width=30, anchor=tk.W, stretch=tk.NO)
            else:
                self.treeview.column(column, width=10, anchor=tk.CENTER)
            self.treeview.heading(column, text=self._lang(column), anchor=tk.CENTER)

    def _init_treeview_scrollbar(self):
        self.logger.debug("\tInitializing treeview scrollbar...")
        scrollbar = ttk.Scrollbar(self.tab, orient=tk.VERTICAL, command=self.treeview.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.treeview.configure(yscrollcommand=scrollbar.set)

    def _init_treeview_menu(self):
        self.logger.debug("\tInitializing treeview menu...")
        self.menu = tk.Menu(self.treeview, tearoff=0)
        self.menu.add_command(label=self._lang('edit'), command=lambda: self.edit_row())
        self.menu.add_command(label=self._lang('delete'), command=lambda: self.delete_row())
        self.treeview.bind('<Button-3>', self.on_right_click)
        self.treeview.bind('<Button-2>', self.on_right_click)
        self.treeview.bind('<Control-Button-1>', self.on_right_click)
        self.treeview.bind('<Double-Button-1>', self.edit_row)

    def populate_treeview(self):
        self.logger.debug("\tPopulating treeview...")
        self.clear_treeview()
        data = self.database.get_all_items(self.name)
        # Capitalize first letter of each element in data lists
        data = [
            [self._lang(item).upper() if isinstance(item, str) else item for item in row]
            for row in data
        ]
        self.logger.debug(f"\t\tData: {data}")
        if data:
            for row in data:
                self.logger.debug(f"\t\tInserting row {row}...")
                self.treeview.insert('', tk.END, values=row)

    def clear_treeview(self):
        self.logger.debug("\tClearing treeview...")
        self.treeview.delete(*self.treeview.get_children())

    def on_right_click(self, event):
        button_state = tk.NORMAL
        try:
            self.treeview.selection_set(self.treeview.identify_row(event.y))
            self.menu.entryconfig(self._lang('delete'), command=lambda: self.delete_row(), state=button_state)
            self.menu.entryconfig(self._lang('edit'), command=lambda: self.edit_row(), state=button_state)
            self.menu.post(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def edit_row(self, event=None):
        pass

    def delete_row(self):
        self.logger.debug(f"\tDeleting row {self.treeview.selection()}...")
        selected_item = self.treeview.selection()
        if selected_item and popup('askyesno', self._lang('delete_item'), self._lang('delete_item_warning')):
            self.logger.debug(f"\t\tSelected item: {selected_item}")
            self.logger.debug(f"\t\tDeleting item {selected_item}...")
            self.database.delete_item(self.name, self.treeview.item(selected_item)['values'][0])
            self.populate_treeview()


class DataWindow(Entity):
    def __init__(self, parent, window_settings):
        super().__init__()
        self.date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.parent = parent
        self.window_config = window_settings.get('config', {})
        self.window_config['window_position'] = \
            f"+{int(parent.root.winfo_x()) + 50}+" \
            f"{int(parent.root.winfo_y()) + 50}"

        self.window_layout = window_settings.get('layout', {})
        self.database = parent.database

        self.entries = {}
        self.error_labels = {}

        self._init_window()

    # ===================================================
    # Layout
    # ===================================================
    def _init_window(self):
        self.logger.debug(f"\tInitializing ticket {self._lang(self.window_config['title'])}...")
        try:
            self.window = tk.Toplevel(self.parent.root, pady=10, padx=10)
            self.window.title(self._lang(self.window_config['title']))
            self.window.geometry(self.window_config['window_size'] + self.window_config['window_position'])
            self.window.resizable(*self.window_config['resizable'])

            self._init_layout()
        except Exception as e:
            self._pop_error('error_loading_window_ticket', str(e))

    def _init_layout(self):
        self.logger.debug("\tInitializing ticket window layout...")
        self._build_sections()
        self._build_notes_section()
        self._build_buttons()

    def _build_sections(self):
        self.logger.debug("\tBuilding sections...")
        for section in self.window_layout:
            self._build_section(section)

    def _build_section(self, section):
        self.logger.debug("\tBuilding section: {}".format(section[0]))
        frame = tk.LabelFrame(self.window, text=self._lang(section[0]))
        frame.grid(row=section[2], column=0, sticky='nsew', padx=5, pady=5)
        frame.grid_columnconfigure(0, minsize=100)
        frame.grid_columnconfigure(1, weight=1)

        for field in section[1]:
            self._build_field(frame, field)

        for i in range(0, len(section[1])):
            frame.grid_rowconfigure(i, weight=1)

    def _build_field(self, frame, field):
        self.logger.debug("\t\tBuilding field: {}".format(field[0]))
        entry = tk.Entry(frame)
        if 'list' in field[0].lower():
            entry = ttk.Combobox(frame, values=[])
        if field[0] == 'date':
            entry.insert(0, self.date)
            entry.configure(state=self.window_config['ticket_date_state'])
        if field[0] == 'notes':
            entry = tk.Text(frame, height=5, width=10, wrap=tk.WORD, pady=5, padx=5)
        if field[0] == 'colorname':
            entry = ttk.Combobox(frame, width=10, values=[self._lang(c).capitalize() for c in self.database.static_values['colors'].values()])
        if field[0] == 'brandname':
            entry = ttk.Combobox(frame, width=10, values=[b.capitalize() for b in self.database.static_values['brands'].values()])
            entry.bind('<<ComboboxSelected>>', self._update_models)
            entry.bind("<Return>", self._update_models)
        if field[0] == 'modelname':
            entry = ttk.Combobox(frame, width=10, values='')
        if 'error' in field[0].lower():
            error_label = tk.Label(frame, text='', fg='red', font=('Arial', 6))
            error_label.grid(row=field[1], column=1, sticky='we', padx=5, pady=(0, 0))
            self.error_labels[field[0]] = error_label
            entry = None
        else:
            label = tk.Label(frame, text=self._lang(field[0]))
            label.grid(row=field[1], column=0, sticky='w', padx=5, pady=5)
            entry.grid(row=field[1], column=1, sticky='we', padx=5, pady=5)

        # Collect entries for later use
        if entry:
            self.entries[field[0]] = entry

    def _update_models(self, event=None):
        self.entries['modelname'].set('')
        brand = self.entries['brandname'].get().lower()
        try:
            models = [m.capitalize() for m in self.database.static_values['models'][brand].values()]
        except KeyError:
            models = []
        self.entries['modelname'].configure(values=models)

    def _build_notes_section(self):
        pass

    def _build_buttons(self):
        frame = tk.Frame(self.window)
        # TODO: Add buttons configuration to window_settings e.g. row number
        frame.grid(row=4, column=0, sticky='w', padx=5, pady=5)
        frame.grid_columnconfigure(1, weight=1)

        ttk.Button(frame, text=self._lang('save'), command=self.save_data).grid(row=0, column=0, sticky='we')
        ttk.Button(frame, text=self._lang('cancel'), command=self.quit_window).grid(row=0, column=1, sticky='we')

    def _pop_error(self, msg, e):
        self.logger.exception(msg, exc_info=True)
        popup('error', self._lang('error'), self._lang(msg) + '\n' + str(e))
        self.quit_window()

    # ===================================================
    # Data validation
    # ===================================================

    def _validate_data(self):
        rc = True
        self.logger.info('* Validating data')
        necessary_entries = ['lastname', 'phone', 'brandname']
        optional_entries = ['vin', 'year', 'email']
        for entry in self.entries:
            if entry in necessary_entries:
                self.logger.debug('\tValidating necessary entry: {}'.format(entry))
                if not self.entries[entry].get():
                    self._data_empty(entry)
                    rc = False
                else:
                    rc = self._validate(self.entries[entry])
            elif entry in optional_entries:
                self.logger.debug('\tValidating optional entry: {}'.format(entry))
                if self.entries[entry].get():
                    rc = self._validate(self.entries[entry])

        return rc

        # if entry in optional_entries and self.entries[entry].get() != '':
        #     if self.entries[entry].get():
        #         self._validate_optional(self.entries[entry])

    @staticmethod
    def _clean_placeholder(entry, event, cc=False):
        """
        Clean placeholder text from entry
        :param entry:  Entry to clean
        :param cc:  Clean color only
        :param event:
        :return: None
        """
        if not cc:
            entry.delete(0, 'end')
        entry.config(foreground='black')
        entry.unbind('<Button-1>')

    def _data_empty(self, entry):
        self._data_invalid(entry, self._lang('field_required'))

    def _validate(self, entry):
        _type = {
            'vin': {
                'error': 'vin_invalid',
                'regex': r'^[A-HJ-NPR-Z0-9]{17}$'
            },
            'email': {
                'error': 'email_invalid',
                'regex': r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            },
            'year': {
                'error': 'year_invalid',
                'regex': r'^[0-9]{4}$'
            },
            'phone': {
                'error': 'phone_invalid',
                'regex': r'^[0-9]{9}$'
            },
            'brandname': {
                'error': 'brand_invalid',
                'regex': r'^[a-zA-Z0-9 ]+$'
            },
            'lastname': {
                'error': 'lastname_invalid',
                'regex': r'^[a-zA-Z0-9 ]+$'
            },
        }

        # Entry is an object of type Entry, Entry is the value of the self.entries dict, we need to get the key
        entry_key = list(self.entries.keys())[list(self.entries.values()).index(entry)]
        if not re.match(_type[entry_key]['regex'], entry.get()):
            self._data_invalid(entry_key, _type[entry_key]['error'])
            return False
        else:
            return True

    def _data_invalid(self, e, error):
        str_entry = f'error_{e}_label'
        label = self.error_labels[str_entry]
        label.config(text=self._lang(error))

    # ===================================================
    # Data Validation END
    # ===================================================

    def get_data_from_entries(self):
        self.logger.info('* Getting data from entries')
        data = {}
        text_box = [tk.Entry, ttk.Combobox]
        if self._validate_data():
            for entry in self.entries:
                data[entry] = self.entries[entry].get() if type(self.entries[entry]) in text_box else \
                    self.entries[entry].get('1.0', 'end-1c')
            return data
        else:
            self.logger.warning('Data validation failed')
            return None

    def save_data(self):
        pass

    def quit_window(self):
        self.logger.info('* Closing window')
        self.window.destroy()


class TicketTreeview(Treeview):
    def __init__(self, tab, column, name, parent):
        super().__init__(tab, column, name, parent)

    def edit_row(self, event=None):
        self.logger.debug(f"\tEditing row {self.treeview.selection()}...")
        selected_item = self.treeview.selection()
        if selected_item:
            self.logger.debug(f"\t\tSelected item: {selected_item}")
            self.logger.debug(f"\t\tEditing item {selected_item}...")
            ticket_id = self.treeview.item(selected_item)["values"][0]
            self.logger.debug(f"\t\t\tTicket ID: {ticket_id}")
            EditTicketWindow(self.parent, ticket_id)


class CustomerTreeview(Treeview):
    def __init__(self, tab, column, name, parent):
        super().__init__(tab, column, name, parent)

    def edit_row(self, event=None):
        self.logger.debug(f"\tEditing row {self.treeview.selection()}...")
        selected_item = self.treeview.selection()
        if selected_item:
            self.logger.debug(f"\t\tSelected item: {selected_item}")
            self.logger.debug(f"\t\tEditing item {selected_item}...")
            customer_id = self.treeview.item(selected_item)["values"][0]
            self.logger.debug(f"\t\t\tCustomer ID: {customer_id}")
            EditCustomerWindow(self.parent, customer_id)


class CarTreeview(Treeview):
    def __init__(self, tab, column, name, parent):
        super().__init__(tab, column, name, parent)

    def edit_row(self, event=None):
        self.logger.debug(f"\tEditing row {self.treeview.selection()}...")
        selected_item = self.treeview.selection()
        if selected_item:
            self.logger.debug(f"\t\tSelected item: {selected_item}")
            self.logger.debug(f"\t\tEditing item {selected_item}...")
            car_id = self.treeview.item(selected_item)["values"][0]
            self.logger.debug(f"\t\t\tCar ID: {car_id}")
            EditCarWindow(self.parent, car_id)


class TreeViewSelector:
    def __init__(self, tab, column, name, parent):
        self.tab = tab
        self.column = column
        self.name = name
        self.parent = parent
        self.treeview = self._run_selector()

    def _run_selector(self):
        tree_view = {
            'tickets': TicketTreeview,
            'customers': CustomerTreeview,
            'cars': CarTreeview
        }
        return tree_view[self.name](self.tab, self.column, self.name, self.parent)

    def save_data(self):
        pass


class NewTicketWindow(DataWindow):
    def __init__(self, parent):
        super().__init__(parent, WINDOWS_SETTINGS['ticket_window'])
        self.logger.info('NewTicketWindow created')
        self.data_type = 'tickets'

    def save_data(self):
        data = self.get_data_from_entries()
        if not data:
            return
        self.logger.info('* Saving data')
        self.logger.debug('\tData: {}'.format(data))
        customer = {}
        car = {}
        ticket = {}
        t_id = None
        if data:
            # Check if customer exists in DB by lastname and phone
            # If not, create new customer and get customer_id
            # If yes, get customer_id
            # customer_id = self.db.get_customer_id(data['lastname'], data['phone'])
            # Check if car exists in DB by customerid
            customer['lastname'] = data.get('lastname')
            customer['phone'] = data.get('phone')
            customer['email'] = data.get('email', '')
            customer['firstname'] = data.get('firstname', '')
            customer_id = self.database.check_if_customer_exists(customer)

            if not customer_id:
                customer_id = self.database.add_item_to_table('customers', customer)

            customer['customerid'] = customer_id
            self.logger.debug('\tCustomer: {}'.format(customer))

            car['brandid'] = self.database.map_name_to_id(data.get('brandname'), 'brands')
            car['modelid'] = self.database.map_name_to_id(data.get('modelname'), 'models')
            car['vin'] = data.get('vin', '')
            car['year'] = data.get('year', '')
            car['colorid'] = data.get('colorname', '').split(' ')[0]
            car['customerid'] = customer['customerid']
            car_id = self.database.check_if_car_exists(car)
            if not car_id:
                car_id = self.database.add_item_to_table('cars', car)
            car['carid'] = car_id
            self.logger.debug('\tCar: {}'.format(car))

            ticket['customerid'] = customer['customerid']
            ticket['carid'] = car['carid']
            ticket['date'] = data.get('date')
            ticket['notes'] = data.get('notes', '')

            self.logger.debug('\tTicket: {}'.format(ticket))
            t_id = self.database.add_item_to_table('tickets', ticket)
            if t_id:
                self.quit_window()
                popup('info', 'Success', self._lang(f'Ticket {t_id} created'))
                self.parent.update_treeviews()


class EditTicketWindow(DataWindow):
    def __init__(self, parent, ticket):
        super().__init__(parent, WINDOWS_SETTINGS['ticket_window'])
        self.logger.info('EditTicketWindow created')
        self._clear_date()
        self.ticket = ticket
        self.fill_data()

    def _clear_date(self):
        self.entries['date'].config(state=tk.NORMAL)
        self.entries['date'].delete(0, 'end')

    def fill_data(self):
        self.logger.info(f'* Filling data with ticket data {self.ticket}')
        self.prepare_data()

    def prepare_data(self):
        self.logger.debug(f"Getting ticket data for ticket ID: {self.ticket}")
        ticket_data = self.database.get_item_from_id('tickets', self.ticket)
        self.logger.debug(f"Ticket data: {ticket_data}")
        customer_data = self.database.get_item_from_id('customers', ticket_data[2])
        car_data = self.database.get_item_from_id('cars', ticket_data[3])
        self.logger.debug(f"Car data: {car_data}")
        brand_data = self.database.static_values['brands'][car_data[2]]
        self.logger.debug(f"Brand data: {brand_data}")
        self.logger.debug(f"{self.database.static_values}")
        self.logger.debug(f"{self.database.static_values['models'][brand_data]}")
        model_data = self.database.static_values['models'][brand_data].get(car_data[3], '')
        color_data = self.database.static_values['colors'].get(car_data[4], '')
        self.logger.debug(f"Customer data: {customer_data}")

        self.logger.debug(f"Brand data: {brand_data}")
        self.logger.debug(f"Model data: {model_data}")

        self.entries['date'].insert(0, ticket_data[1])

        self.entries['firstname'].insert(0, customer_data[1])
        self.entries['lastname'].insert(0, customer_data[2])
        self.entries['phone'].insert(0, customer_data[3])
        self.entries['email'].insert(0, customer_data[4])

        self.entries['brandname'].insert(0, brand_data.capitalize())
        self.entries['modelname'].insert(0, model_data)
        self.entries['year'].insert(0, car_data[5])
        self.entries['colorname'].insert(0, color_data.capitalize())
        self.entries['vin'].insert(0, car_data[6])

        self.entries['notes'].insert(tk.END, ticket_data[4])

    def save_data(self):
        data = self.get_data_from_entries()
        self.logger.debug(f"Data: {data}")
        customer = {}
        car = {}
        ticket = {}

        customer['lastname'] = data.get('lastname')
        customer['phone'] = data.get('phone')
        customer['email'] = data.get('email', '')
        customer['firstname'] = data.get('firstname', '')
        customer_id = self.database.check_if_customer_exists(customer)
        if not customer_id:
            rc = popup('askyesno', 'Question', self._lang('add_customer'))
            if rc:
                customer_id = self.database.add_item_to_table('customers', customer)
        customer['customerid'] = customer_id
        self.logger.debug('\tCustomer: {}'.format(customer))

        car['brandid'] = self.database.map_name_to_id(data.get('brandname'), 'brands')
        car['modelid'] = self.database.map_name_to_id(data.get('modelname'), 'models')
        car['vin'] = data.get('vin', '')
        car['year'] = data.get('year', '')
        car['colorid'] = data.get('colorname', '').split(' ')[0]
        car['customerid'] = customer['customerid']
        car_id = self.database.check_if_car_exists(car)
        if not car_id:
            rc = popup('askyesno', 'Question', self._lang('ask_add_car'))
            if rc:
                car_id = self.database.add_item_to_table('cars', car)
        car['carid'] = car_id
        self.logger.debug('\tCar: {}'.format(car))

        ticket['customerid'] = customer['customerid']
        ticket['carid'] = car['carid']
        ticket['date'] = data.get('date')
        ticket['notes'] = data.get('notes', '')
        ticket['ticketid'] = self.ticket

        self.logger.debug('\tTicket: {}'.format(ticket))
        self.database.update_ticket(ticket)
        self.quit_window()
        popup('info', 'Success', self._lang(f'Ticket {self.ticket} updated'))
        self.parent.update_treeviews()


class EditCustomerWindow(DataWindow):
    def __init__(self, parent, customer_id):
        super().__init__(parent, WINDOWS_SETTINGS['edit_customer_window'])
        self.logger.info('EditCustomerWindow created')
        self.customer_id = customer_id
        self.current_customer_data = None

        self.fill_data()

    def fill_data(self):
        self.logger.info(f'* Filling data with customer data {self.customer_id}')
        self.prepare_data()

    def prepare_data(self):
        customer_data = self.database.get_item_from_id('customers', self.customer_id)
        self.logger.debug(f"Customer data: {customer_data}")
        self.entries['firstname'].insert(0, customer_data[1])
        self.entries['lastname'].insert(0, customer_data[2])
        self.entries['email'].insert(0, customer_data[3])
        self.entries['phone'].insert(0, customer_data[4])
        self.entries['car_list'].set(self._lang('not_implemented'))
        self.current_customer_data = customer_data

    def save_data(self):
        data = self.get_data_from_entries()

        if not self._validate_data():
            self.logger.warning('Data validation failed')
            return
        self.logger.debug(f"Data from entries: {data}")

        # Update customer data
        customer = {
            'customerid': self.customer_id,
            'firstname': data.get('firstname', ''),
            'lastname': data.get('lastname'),
            'email': data.get('email', ''),
            'phone': data.get('phone'),
        }
        self.logger.debug(f"Customer data: {customer}")
        self.database.update_customer(customer)
        self.quit_window()
        popup('info', 'Success', self._lang(f'Customer {self.customer_id} updated'))
        self.parent.update_treeviews()


class EditCarWindow(DataWindow):
    def __init__(self, parent, car_id):
        super().__init__(parent, WINDOWS_SETTINGS['edit_car_window'])
        self.logger.info('EditCarWindow created')
        self.car_id = car_id

        self.fill_data()
        self.current_car_data = None

    def fill_data(self):
        self.logger.info(f'* Filling data with car data {self.car_id}')
        self.prepare_data()

    def prepare_data(self):
        car_data = self.database.get_item_from_id('cars', self.car_id)
        self.logger.debug(f"Car data: {car_data}")
        brand_data = self.database.static_values['brands'].get(car_data[2], '').capitalize()
        self.logger.debug(f"Brand data: {brand_data}")
        model_data = self.database.static_values['models'][brand_data.lower()].get(car_data[3], '')
        color_data = self.database.static_values['colors'].get(car_data[4], '')
        customer_data = self.database.get_item_from_id('customers', car_data[1])
        customer_data = f"{customer_data[2]} ({customer_data[4]})"
        self.logger.debug(f"Model data: {model_data}")

        self.entries['brandname'].insert(0, brand_data)
        self._update_models()
        self.entries['modelname'].insert(0, model_data)
        self.entries['year'].insert(0, car_data[5])
        self.entries['colorname'].insert(0, color_data.capitalize())
        self.entries['vin'].insert(0, car_data[6])
        self.entries['customer'].insert(0, customer_data)
        self.entries['customer'].config(state='disabled')

        self.current_car_data = car_data

    def save_data(self):
        data = self.get_data_from_entries()
        self.logger.debug(f"Data from entries: {data}")
        if not self._validate_data():
            self.logger.warning('Data validation failed')
            return

        # Update car data
        car = {
            'carid': self.car_id,
            'brandid': self.database.map_name_to_id(data.get('brandname', '').lower(), 'brands'),
            'modelid': self.database.map_name_to_id(data.get('modelname', ''), 'models'),
            'year': data.get('year', ''),
            'colorid': self.database.map_name_to_id(data.get('colorname', '').lower(), 'colors'),
            'vin': data.get('vin', ''),
        }
        self.logger.debug(f"Car data: {car}")
        self.database.update_car(car)
        self.quit_window()
        popup('info', 'Success', self._lang(f'Car {self.car_id} updated'))
        self.parent.update_treeviews()
