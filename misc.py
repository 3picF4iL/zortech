import logging
import tkinter as tk
from tkinter import ttk


LANG = {
    'en': {
        'exit': 'Exit',
        'new_ticket': 'New ticket',
        'import_db': 'Import database',
        'export_db': 'Export database',
        'current_entries': 'Current entries',
        'date': 'Date',
        'time': 'Time',
        'name': 'Name',
        'surname': 'Surname',
        'phone': 'Phone',
        'email': 'Email',
        'description': 'Description',
        'status': 'Status',
        'edit': 'Edit',
        'delete': 'Delete',
        'save': 'Save',
        'cancel': 'Cancel',
        'save_changes': 'Save changes',
        'cancel_changes': 'Cancel changes',
        'add': 'Add',
        'edit_entry': 'Edit entry',
        'delete_entry': 'Delete entry',
        'add_entry': 'Add entry',
    },
    'pl': {
        'exit': 'Wyjście',
        'new_ticket': 'Nowe zgłoszenie',
        'import_db': 'Importuj bazę danych',
        'export_db': 'Wyeksportuj bazę danych',
        'current_entries': 'Aktualne zgłoszenia',
        'date': 'Data',
        'time': 'Godzina',
        'name': 'Imię',
        'surname': 'Nazwisko',
        'phone': 'Telefon',
        'email': 'Email',
        'description': 'Opis',
        'status': 'Status',
        'edit': 'Edytuj',
        'delete': 'Usuń',
        'save': 'Zapisz',
        'cancel': 'Anuluj',
        'save_changes': 'Zapisz zmiany',
        'cancel_changes': 'Anuluj zmiany',
        'add': 'Dodaj',
        'edit_entry': 'Edytuj zgłoszenie',
        'delete_entry': 'Usuń zgłoszenie',
        'edit_entry_text': 'Edytujesz zgłoszenie o numerze: ',
        'delete_entry_text': 'Czy na pewno chcesz usunąć zgłoszenie o numerze: ',
        'notes': 'Uwagi',
        'add_note': 'Dodaj notatkę',
        'edit_note': 'Edytuj notatkę',
        'delete_note': 'Usuń notatkę',
        'edit_note_text': 'Edytujesz notatkę o numerze: ',
        'file': 'Plik',
        'car': 'Pojazd',
        'vin': 'VIN',
        'id': 'ID',
        'customer': 'Klient',
        'ticket': 'Zgłoszenie',
        'customer_firstname': 'Imię',
        'customer_lastname': 'Nazwisko',
        'customer_phone': 'Telefon',
        'customer_email': 'Email',
        'brand': 'Marka',
        'model': 'Model',
        'year': 'Rok',
        'color': 'Kolor',
        'black': 'Czarny',
        'white': 'Biały',
        'red': 'Czerwony',
        'blue': 'Niebieski',
        'green': 'Zielony',
        'yellow': 'Żółty',
        'orange': 'Pomarańczowy',
        'silver': 'Srebrny',
        'gold': 'Złoty',
        'grey': 'Szary',
        'other': 'Inny',
    },
    'pl_en': {
        'srebrny': 'silver',
        'złoty': 'gold',
        'szary': 'grey',
        'czarny': 'black',
        'biały': 'white',
        'czerwony': 'red',
        'niebieski': 'blue',
        'zielony': 'green',
        'żółty': 'yellow',
        'pomarańczowy': 'orange',
        'inny': 'other',
        'marka': 'brand',
        'model': 'model',
        'rok': 'year',
        'kolor': 'color',
        'imie': 'name',
        'nazwisko': 'surname',
        'telefon': 'phone',
        'email': 'email',
        'opis': 'description',
        'status': 'status',
        'edycja': 'edit',
        'usuń': 'delete',
        'zapisz': 'save',
        'anuluj': 'cancel',
        'zapisz zmiany': 'save changes',
    }
}

TICKET_WINDOW_CONFIG = {
            'title': 'new_ticket',
            'resizable': (True, True),
            'ticket_date_state': 'readonly'
            #'icon': 'icons/ticket.ico',
            #'bg': '#f0f0f0',
            #'font': ('Arial', 10)
 }

TICKET_WINDOW_LAYOUT = {
    '--': [
        ("date:", 0),
    ],
    'customer': [
        ("name:", 0),
        ("surname:", 1),
        ("phone:", 2),
        ("email:", 3)
    ],
    'car': [
        ("brand:", 0),
        ("model:", 1),
        ("year:", 2),
        ("color:", 3),
        ("vin:", 4)
    ]
}

APP_CONFIG = {
            "version": "0.1",
            "author": "ZORTECH",
            "author_email": "",
            "title": "ZORTECH Serwis Klimatyzacji Samochodowej",
            "geometry": "800x600",
            "lang": "pl",
}


class AutocompleteCombobox(ttk.Combobox):
    def __init__(self, parent):
        super().__init__(parent)

    def set_completion_list(self, completion_list):
        """Use our completion list as our drop down selection menu, arrows move through menu."""
        self._completion_list = sorted(completion_list, key=str.lower)  # Work with a sorted list
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)
        self['values'] = self._completion_list  # Setup our popup menu

    def autocomplete(self, delta=0):
        """autocomplete the Combobox, delta may be 0/1/-1 to cycle through possible hits"""
        if delta:  # need to delete selection otherwise we would fix the current position
            self.delete(self.position, tk.END)
        else:  # set position to end so selection starts where textentry ended
            self.position = len(self.get())
        # collect hits
        _hits = []
        for element in self._completion_list:
            if element.lower().startswith(self.get().lower()):  # Match case insensitively
                _hits.append(element)
        # if we have a new hit list, keep this in mind
        if _hits != self._hits:
            self._hit_index = 0
            self._hits = _hits
        # only allow cycling if we are in a known hit list
        if _hits == self._hits and self._hits:
            self._hit_index = (self._hit_index + delta) % len(self._hits)
        # now finally perform the auto completion
        if self._hits:
            self.delete(0, tk.END)
            self.insert(0, self._hits[self._hit_index])
            self.select_range(self.position, tk.END)

    def handle_keyrelease(self, event):
        """event handler for the keyrelease event on this widget"""
        if event.keysym == "BackSpace":
            self.delete(self.index(tk.INSERT), tk.END)
            self.position = self.index(tk.END)
        if event.keysym == "Left":
            if self.position < self.index(tk.END):  # delete the selection
                self.delete(self.position, tk.END)
            else:
                self.position = self.position - 1  # delete one character
                self.delete(self.position, tk.END)
        if event.keysym == "Right":
            self.position = self.index(tk.END)  # go to end (no selection)
        if len(event.keysym) == 1:
            self.autocomplete()
        # No need for up/down, we'll jump to the popup
        # list at the position of the autocompletion

import logging

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
