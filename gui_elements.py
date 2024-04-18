from misc import (
    Entity,
    WINDOWS_SETTINGS,
    Logger,
    popup)
import datetime
import tkinter as tk
import re
from tkinter import ttk
from entities import *


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
        self.menu.add_separator()
        self.menu.add_command(label=self._lang('change_status'), command=lambda: self.change_status())
        self.treeview.bind('<Button-3>', self.on_right_click)
        self.treeview.bind('<Button-2>', self.on_right_click)
        self.treeview.bind('<Control-Button-1>', self.on_right_click)
        self.treeview.bind('<Double-Button-1>', self.edit_row)

    def populate_treeview(self):
        # FIXME: Refactor this function it is ugly
        tag = ''
        self.logger.debug("\tPopulating treeview...")
        style = ttk.Style()
        style.map('Treeview', background=[('selected', '#999999')])
        self.treeview.tag_configure('Green.Row', background='#E6FFE6')
        self.treeview.tag_configure('Red.Row', background='#FFE6E6')
        self.clear_treeview()
        data = self.database.get_all_items(self.name)
        # Capitalize first letter of each element in data lists
        data = [
            [item.upper() if isinstance(item, str) else item for item in row]
            for row in data
        ]
        if data:
            for row in data:
                # Set color row depends on the last value from data (status 1/0 where 1 is not done)w
                if self.name == 'tickets':
                    tag = 'Green.Row' if row[-1] == 0 else 'Red.Row'
                self.treeview.insert('', tk.END, values=row, tags=tag)
        else:
            self.logger.debug("\t\tNo data to populate treeview...")

    def clear_treeview(self):
        self.logger.debug("\tClearing treeview...")
        self.treeview.delete(*self.treeview.get_children())

    def on_right_click(self, event):
        # FIXME: Refactor this function, do we really need duplicated code?
        button_state = tk.DISABLED
        try:
            row_id = self.treeview.identify_row(event.y)
            if row_id:
                button_state = tk.NORMAL
                self.treeview.selection_set(row_id)
                self.menu.entryconfig(self._lang('delete'), command=lambda: self.delete_row(), state=button_state)
                self.menu.entryconfig(self._lang('edit'), command=lambda: self.edit_row(), state=button_state)
                self.menu.entryconfig(self._lang('change_status'), command=lambda: self.change_status(), state=button_state)
                self.menu.post(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def edit_row(self, event=None):
        pass

    def change_status(self, event=None):
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
        if 'date_creation' in field[0]:
            if not self.window_config['title'] == 'edit_ticket':
                entry.insert(0, self.date)
            entry.configure(state=self.window_config['ticket_date_state'])
        if field[0] == 'notes':
            entry = tk.Text(frame, height=5, width=10, wrap=tk.WORD, pady=5, padx=5)
        if field[0] == 'color_name':
            entry = ttk.Combobox(frame, width=10, values=[c[1].upper() for c in self.database.fetch_colors()])
        if field[0] == 'brand_name':
            entry = ttk.Combobox(frame, width=10, values=[b[1].upper() for b in self.database.fetch_brands()])
            entry.bind('<<ComboboxSelected>>', self._update_models)
            entry.bind("<Return>", self._update_models)
        if field[0] == 'model_name':
            entry = ttk.Combobox(frame, width=10, values=('',))
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
        self.logger.debug("Update models")
        self.entries['model_name'].set('')
        brand = self.entries['brand_name'].get().lower()
        try:
            models = [m[0].upper() for m in self.database.fetch_models_from_brand(brand)]
        except KeyError:
            models = []
        self.entries['model_name'].configure(values=models)

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
        necessary_entries = ['last_name', 'phone', 'brand_name']
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
            'brand_name': {
                'error': 'brand_invalid',
                'regex': r'^[a-zA-Z0-9 ]+$'
            },
            'last_name': {
                'error': 'last_name_invalid',
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

    def change_status(self, event=None):
        status = 1
        ticket_id = self.treeview.item(self.treeview.selection())["values"][0]
        if ticket_id:
            current_ticket_status = self.database.get_item_from_id('tickets', ticket_id, columns='status')
            print(current_ticket_status)
            if bool(current_ticket_status['status']):
                status = 0

            self.database.update_ticket({'id': ticket_id, 'status': status})
        self.populate_treeview()


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

        customer = Customer({
            'first_name': data.get('first_name', '').lower(),
            'last_name': data.get('last_name', '').lower(),
            'phone':  data.get('phone', '').lower(),
            'email':  data.get('email', '').lower()
        }, self.database)
        customer.add()

        car = Car({
            'brand_id': self.database.get_item_from_name('brands', data.get('brand_name').lower()),
            'model_id': self.database.get_item_from_name('models', data.get('model_name').lower()),
            'vin': data.get('vin', ''),
            'year': data.get('year', ''),
            'color_id': self.database.get_item_from_name('colors', data.get('color_name').lower()),
            'customer_id': customer.get_id(),
        }, self.database)
        car.add()

        ticket = Ticket({
            'customer_id': customer.get_id(),
            'car_id': car.get_id(),
            'date_creation': data.get('date_creation'),
            'date_modification': data.get('date_modification'),
            'notes': data.get('notes', ''),
            'status': data.get('status', '')
        }, self.database)
        ticket.add()

        self.quit_window()
        self.parent.update_treeviews()
        if ticket.get_id():
            popup('info', 'Success', self._lang(f'Ticket {ticket.get_id()} created'))
        else:
            popup('error', 'Error', "Ticket could not be created!")


class EditTicketWindow(DataWindow):
    def __init__(self, parent, ticket):
        super().__init__(parent, WINDOWS_SETTINGS['edit_ticket_window'])
        self.logger.info('EditTicketWindow created')
        self.data = None
        self.car = None
        self.customer = None
        self.ticket = ticket
        self._read_ticket_data()

    def _read_ticket_data(self):
        # TODO: This should be moved and refactored
        self.data = self.database.get_item_from_id('tickets', self.ticket)
        ticket = TicketDAO(self.data, self.database)
        self.customer = CustomerDAO(self.data, self.database)
        self.car = CarDAO(self.data, self.database)

        self.entries['date_creation'].configure(state='normal')
        self.entries['date_creation'].insert(0, ticket.date_creation)
        self.entries['date_creation'].configure(state='disable')
        self.entries['date_modification'].insert(0, self.date)

        self.entries['first_name'].insert(0, self.customer.collected_data['first_name'].capitalize())
        self.entries['last_name'].insert(0, self.customer.collected_data['last_name'].capitalize())
        self.entries['phone'].insert(0, self.customer.collected_data['phone'])
        self.entries['email'].insert(0, self.customer.collected_data['email'].upper())

        self.entries['brand_name'].insert(0, self.database.get_item_from_id('brands',
                                                                            self.car.collected_data['brand_id']
                                                                            )['name'].upper())
        self._update_models()
        self.entries['model_name'].insert(0, self.database.get_item_from_id('models',
                                                                            self.car.collected_data['model_id']
                                                                            )['name'].upper())
        self.entries['year'].insert(0, self.car.collected_data['year'])
        self.entries['color_name'].insert(0, self.database.get_item_from_id('colors',
                                                                            self.car.collected_data['color_id']
                                                                            )['name'].upper())
        self.entries['vin'].insert(0, self.car.collected_data['vin'].upper())

        self.entries['notes'].insert(tk.END, ticket.notes)

    def save_data(self):
        # TODO: Remove duplicated code (compare this to other functions - save_data)
        data = self.get_data_from_entries()
        if not data:
            return
        customer = Customer({
            'id': self.customer.id,
            'first_name': data.get('first_name', '').lower(),
            'last_name': data.get('last_name', '').lower(),
            'phone':  data.get('phone', ''),
            'email':  data.get('email', '').lower(),
        }, self.database)
        customer.update()

        car = Car({
            'id': self.car.id,
            'brand_id': self.database.get_item_from_name('brands', data.get('brand_name')),
            'model_id': self.database.get_item_from_name('models', data.get('model_name')),
            'vin': data.get('vin', ''),
            'year': data.get('year', ''),
            'color_id': self.database.get_item_from_name('colors', data.get('color_name')),
            'customer_id': customer.get_id(),
        }, self.database)
        car.update()

        ticket = Ticket({
            'id': self.ticket,
            'customer_id': customer.get_id(),
            'car_id': car.get_id(),
            'date_creation': data.get('date_creation'),
            'date_modification': data.get('date_modification'),
            'notes': data.get('notes', '')
        }, self.database)
        ticket.update()

        self.quit_window()
        self.parent.update_treeviews()
        popup('info', 'Success', self._lang(f'Ticket {self.ticket} updated'))


class EditCustomerWindow(DataWindow):
    def __init__(self, parent, customer_id):
        super().__init__(parent, WINDOWS_SETTINGS['edit_customer_window'])
        self.logger.info('EditCustomerWindow created')
        self.customer_id = customer_id

        self._read_customer_data()

    def _get_customer_cars(self):
        # FIXME: Maybe we should create a separate function for this?
        customer_cars = self.database.fetch_all_join('cars',
                                                     columns='brands.id AS brand_id, models.id AS model_id',
                                                     join='''
                                                     brands
                                                     ON cars.brand_id = brands.id
                                                     LEFT JOIN models
                                                     ON cars.model_id = models.id
                                                     LEFT JOIN colors
                                                     ON cars.color_id = colors.id
                                                     ''',
                                                     where=f'customer_id = {self.customer_id}',
                                                     dictionary=True)
        customer_car_info = [
            (f"{self.database.get_item_from_id('brands', brand['brand_id'])['name'].upper()}"
             f" {self.database.get_item_from_id('models', brand['model_id'])['name'].upper()}")
            for brand in customer_cars
        ]
        return customer_car_info

    def _read_customer_data(self):
        self.logger.info(f'* Read customer data with customer ID: {self.customer_id}')
        customer_data = self.database.get_item_from_id('customers', self.customer_id)
        self.logger.debug(f"Customer data: {customer_data}")
        self.entries['first_name'].insert(0, customer_data['first_name'].capitalize())
        self.entries['last_name'].insert(0, customer_data['last_name'].capitalize())
        self.entries['email'].insert(0, customer_data['email'].upper())
        self.entries['phone'].insert(0, customer_data['phone'])

        self.entries['car_list'].configure(values=self._get_customer_cars())

    def save_data(self):
        data = self.get_data_from_entries()

        if not self._validate_data():
            self.logger.warning('Data validation failed')
            return
        self.logger.debug(f"Data from entries: {data}")

        # Update customer data
        customer = {
            'id': self.customer_id,
            'first_name': data.get('first_name', '').lower(),
            'last_name': data.get('last_name').lower(),
            'email': data.get('email', '').lower(),
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

        self._read_car_data()

    def _read_car_data(self):
        self.logger.info(f'* Reading data for car with ID: {self.car_id}')
        car_data = self.database.get_item_from_id('cars', self.car_id)

        self.entries['brand_name'].insert(0, self.database.get_item_from_id('brands',
                                                                            car_data['brand_id']
                                                                            )['name'].upper())
        self._update_models()
        self.entries['model_name'].insert(0, self.database.get_item_from_id('models',
                                                                            car_data['model_id']
                                                                            )['name'].upper())
        self.entries['year'].insert(0, car_data['year'])
        self.entries['color_name'].insert(0, self.database.get_item_from_id('colors',
                                                                            car_data['color_id']
                                                                            )['name'].upper())
        self.entries['vin'].insert(0, car_data['vin'])
        customer_data = self.database.get_item_from_id('customers', car_data['customer_id'])
        self.entries['customer'].insert(0,
                                        (f"{customer_data['first_name'].capitalize()} "
                                         f"{customer_data['last_name'].capitalize()} "
                                         f"{customer_data['phone']}"))
        self.entries['customer'].config(state='disabled')

    def save_data(self):
        data = self.get_data_from_entries()
        self.logger.debug(f"Data from entries: {data}")
        if not self._validate_data():
            self.logger.warning('Data validation failed')
            return

        # Update car data
        car = {
            'id': self.car_id,
            'brand_id': self.database.get_item_from_name('brands', data.get('brand_name')),
            'model_id': self.database.get_item_from_name('models', data.get('model_name')),
            'year': data.get('year', ''),
            'color_id': self.database.get_item_from_name('colors', data.get('color_name')),
            'vin': data.get('vin', ''),
        }
        self.logger.debug(f"Car data: {car}")
        self.database.update_car(car)
        self.quit_window()
        self.parent.update_treeviews()
        popup('info', 'Success', self._lang(f'Car {self.car_id} updated'))

