import logging
from tkinter import messagebox
from lang import LANG


class Entity:
    def __init__(self):
        self.app_config = APP_CONFIG
        self.app_lang = self.app_config.get('lang', 'pl')
        self.logger = Logger.get_logger(self.__class__.__name__)

    def _lang(self, expression):
        return LANG[self.app_lang].get(expression, expression)


APP_CONFIG = {
    "version": "0.1",
    "author": "ZORTECH",
    "author_email": "",
    "title": "ZORTECH Serwis Klimatyzacji Samochodowej",
    "geometry": "1440x600",
    "lang": "pl",
    "layout_config": {
        "normal_font": ('Segoe UI', 9),
        "large_font": ('Segoe UI', 12),
    },
}

TICKET_WINDOW_CONFIG = {
    'title': 'new_ticket',
    'resizable': (True, True),
    'ticket_date_state': 'readonly',
    'window_size': '270x750',
    #'icon': 'icons/ticket.ico',
    #'bg': '#f0f0f0',
    #'font': ('Arial', 10)
 }

TICKET_WINDOW_LAYOUT = [
    [
        '--',
        [
            ("date", 0)
        ],
        0  # row
    ],
    [
        'customer',
        [
            ("firstname", 0),
            ("error_firstname_label", 1),
            ("lastname", 2),
            ("error_lastname_label", 3),
            ("phone", 4),
            ("error_phone_label", 5),
            ("email", 6),
            ("error_email_label", 7),
        ],
        1  # row
    ],
    [
        'car',
        [
            ("brandname", 0),
            ("error_brandname_label", 1),
            ("modelname", 2),
            ("error_modelname_label", 3),
            ("year", 4),
            ("error_year_label", 5),
            ("colorname", 6),
            ("error_colorname_label", 7),
            ("vin", 8),
            ("error_vin_label", 9),
        ],
        2  # row
    ],
    [
        'notes',
        [
            ("notes", 0)
        ],
        3  # row
    ]
]

TICKET_WINDOW_LAYOUT_JSON = [
    {
        "label": "--",
        "fields": [
            {"name": "date", "position": 0}
        ],
        "row": 0
    },
    {
        "label": "customer",
        "fields": [
            {"name": "firstname", "position": 0},
            {"name": "lastname", "position": 1},
            {"name": "phone", "position": 2},
            {"name": "email", "position": 3}
        ],
        "row": 1
    },
    {
        "label": "car",
        "fields": [
            {"name": "brandname", "position": 0},
            {"name": "modelname", "position": 1},
            {"name": "year", "position": 2},
            {"name": "colorname", "position": 3},
            {"name": "vin", "position": 4}
        ],
        "row": 2
    },

]

TICKET_WINDOW_EVENT_BINDINGS = ['<Button-1>', '<Enter>', '<Tab>']

EDIT_CUSTOMER_WINDOW_LAYOUT = [
    [
        'customer',
        [
            ("firstname", 0),
            ("error_firstname_label", 1),
            ("lastname", 2),
            ("error_lastname_label", 3),
            ("phone", 4),
            ("error_phone_label", 5),
            ("email", 6),
            ("error_email_label", 7),
        ],
        0  # row
    ],
    [
        'cars',
        [
            ("car_list", 0)
        ],
        1  # row
    ]
]

EDIT_CUSTOMER_WINDOW_CONFIG = {
    'title': 'edit_customer',
    'resizable': (True, True),
    'window_size': '280x400',
    #'icon': 'icons/ticket.ico',
    #'bg': '#f0f0f0',
    #'font': ('Arial', 10)
    }

EDIT_CAR_WINDOW_LAYOUT = [
    [
        'car',
        [
            ("brandname", 0),
            ("error_brandname_label", 1),
            ("modelname", 2),
            ("error_modelname_label", 3),
            ("year", 4),
            ("error_year_label", 5),
            ("colorname", 6),
            ("error_colorname_label", 7),
            ("vin", 8),
            ("error_vin_label", 9),
        ],
        0  # row
    ],
    [
        'owner',
        [
            ("customer", 0),
        ],
        1  # row
    ]
]

EDIT_CAR_WINDOW_CONFIG = {
    'title': 'edit_car',
    'resizable': (True, True),
    'window_size': '280x400',
    #'icon': 'icons/ticket.ico',
    #'bg': '#f0f0f0',
    #'font': ('Arial', 10)
    }



WINDOWS_SETTINGS = {
    'ticket_window': {
        'config': TICKET_WINDOW_CONFIG,
        'layout': TICKET_WINDOW_LAYOUT,
        'event_bindings': TICKET_WINDOW_EVENT_BINDINGS
    },
    'edit_customer_window': {
        'config': EDIT_CUSTOMER_WINDOW_CONFIG,
        'layout': EDIT_CUSTOMER_WINDOW_LAYOUT,
        'event_bindings': []
    },
    'edit_car_window': {
        'config': EDIT_CAR_WINDOW_CONFIG,
        'layout': EDIT_CAR_WINDOW_LAYOUT,
        'event_bindings': []
    }
}


class Logger:
    @staticmethod
    def setup_logging():
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

        file_handler = logging.FileHandler('zortechapp.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)

        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)

        root_logger.propagate = False

    @staticmethod
    def get_logger(name):
        return logging.getLogger(name)


def popup(m_type, title, msg):
    _type = {
        'info': messagebox.showinfo,
        'warning': messagebox.showwarning,
        'error': messagebox.showerror,
        'question': messagebox.askquestion,
        'okcancel': messagebox.askokcancel,
        'askyesno': messagebox.askyesno,
    }

    out = _type[m_type](title, msg)
    return out


