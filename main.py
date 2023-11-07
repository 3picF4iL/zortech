from datetime import datetime
from database import Database
from gui import GUIApp


class MainApplication:
    def __init__(self):
        # Create main window (layout/GUI)
        # Connect to database and fetch data
        # Use data to populate treeview
        self.app_config = {
            "version": "0.1",
            "author": "ZORTECH",
            "author_email": "",
            "title": "ZORTECH Serwis Klimatyzacji Samochodowej",
            "geometry": "800x600",
        }
        self.data_base_name = "zortech.db"
        self.db = Database(self.data_base_name)
        self.gui = GUIApp(self.app_config, self.db)

        # FIXME: Enable displaying data
        # self.display_data()

        self.gui.root.mainloop()


    def open_new_ticket_window(self):
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        new_ticket_window = tk.Toplevel()
        new_ticket_window.geometry("600x300")
        new_ticket_window.title("Nowe Zgłoszenie")

        main_frame = tk.Frame(new_ticket_window)
        main_frame.pack(fill="both", padx=10, pady=5, expand=False)

        frame_left = tk.Frame(self.main_frame)
        frame_left.pack(side="left", padx=5, fill="both", expand=False)

        frame_left_label = tk.Frame(self.frame_left)
        frame_left_label.pack(side="left", fill="both", expand=False, padx=5,)
        frame_left_entry = tk.Frame(self.frame_left)
        frame_left_entry.pack(side="right", fill="both", expand=False)

        frame_right = tk.Frame(self.main_frame)
        frame_right.pack(side="right", padx=5, fill="both", expand=False)

        frame_right_label = tk.Frame(self.frame_right)
        frame_right_label.pack(side="left", fill="both", expand=False)
        frame_right_entry = tk.Frame(self.frame_right)
        frame_right_entry.pack(side="right", fill="both", expand=False)

        date_label = tk.Label(self.frame_left_label, text="Data zgłoszenia:")
        date_label.pack(padx=5, pady=5)
        date_entry = tk.Entry(self.frame_left_entry)
        date_entry.insert(0, date)
        date_entry.config(state="readonly")
        date_entry.pack(padx=5, pady=5)

        client_name_label = tk.Label(self.frame_left_label, text="Imię i nazwisko klienta:")
        client_name_label.pack(padx=5, pady=5)
        client_name_entry = tk.Entry(self.frame_left_entry)
        client_name_entry.pack(padx=5, pady=5)

        car_model_label = tk.Label(self.frame_left_label, text="Model samochodu:")
        car_model_label.pack(padx=5, pady=5)
        car_model_entry = tk.Entry(self.frame_left_entry)
        car_model_entry.pack(padx=5, pady=5)

        year_label = tk.Label(self.frame_left_label, text="Rok produkcji:")
        year_label.pack(padx=5, pady=5)
        year_entry = tk.Entry(self.frame_left_entry)
        year_entry.pack(padx=5, pady=5)

        vin_label = tk.Label(frame_left_label, text="Numer VIN:")
        vin_label.pack(padx=5, pady=5)
        vin_entry = tk.Entry(self.frame_left_entry)
        vin_entry.pack(padx=5, pady=5)

        notes_label = tk.Label(self.frame_right_label, text="Uwagi:")
        notes_label.pack(side=tk.TOP, padx=5, pady=5)
        notes_entry = tk.Text(self.frame_right_entry, width=20, height=10)
        notes_entry.pack(padx=5, pady=5, fill='both', expand=True)

        data = {
            "date": date_entry,
            "client_name": client_name_entry,
            "car_model": car_model_entry,
            "year": year_entry,
            "vin": vin_entry,
            "notes": notes_entry
        }

        frame_bottom = tk.Frame(self.new_ticket_window)
        frame_bottom.pack(pady=10)

        save_button = tk.Button(self.frame_bottom, text="Zapisz", command=lambda: self.save_ticket(new_ticket_window, data))
        save_button.pack(side=tk.LEFT, padx=5, pady=5)
        cancel_button = tk.Button(self.frame_bottom, text="Anuluj", command=new_ticket_window.destroy)
        cancel_button.pack(side=tk.LEFT, padx=5, pady=5)

        new_ticket_window.mainloop()

    def save_ticket(self, w, data):
        conn = sqlite3.connect('service.db')
        c = conn.cursor()

        date = data["date"].get()
        client_name = data["client_name"].get()
        car_model = data["car_model"].get()
        year = data["year"].get()
        vin = data["vin"].get()
        notes = data["notes"].get("1.0", "end-1c")

        c.execute("INSERT INTO tickets "
                  "(date, client_name, car_model, year, vin, notes) VALUES (?, ?, ? ,?, ?, ?)",
                  (date, client_name, car_model, year, vin, notes))
        conn.commit()
        conn.close()

        display_data()
        w.destroy()
        show_popup("info", "Zgłoszenie", "Zgłoszenie zostało zapisane")


    # def create_tables():
    #     conn = sqlite3.connect('service.db')
    #     c = conn.cursor()
    #
    #     # Delete table if exists and create new one
    #     c.execute("DROP TABLE IF EXISTS clients")
    #     c.execute("DROP TABLE IF EXISTS tickets")
    #     c.execute('''CREATE TABLE tickets (id INTEGER PRIMARY KEY,
    #             date TEXT,
    #             client_name TEXT,
    #             car_model TEXT,
    #             year INTEGER,
    #             vin TEXT,
    #             notes TEXT
    #         )''')
    #     conn.commit()
    #     conn.close()
    #     display_data()


# def setup_database():
#     conn = sqlite3.connect('service.db')
#     c = conn.cursor()
#
#     c.execute('''CREATE TABLE IF NOT EXISTS clients
#                  (id INTEGER PRIMARY KEY, name TEXT, car_model TEXT, vin TEXT)''')
#     c.execute('''CREATE TABLE IF NOT EXISTS tickets
#                  (id INTEGER PRIMARY KEY, client_id INTEGER, date TEXT, notes TEXT,
#                  FOREIGN KEY(client_id) REFERENCES clients(id))''')
#
#     c.execute("INSERT INTO clients (name, car_model, vin) VALUES ('Jan Kowalski', 'Toyota Corolla', 'VIN123456')")
#     conn.commit()
#     conn.close()


    def delete_entry(self, event):
        selected_item = tree.identify_row(event.y)
        if selected_item:
            tree.delete(selected_item)
            conn = sqlite3.connect('service.db')
            c = conn.cursor()
            c.execute("DELETE FROM tickets WHERE id=?", (selected_item,))
            conn.commit()
            conn.close()


    def edit_window(self, conn, c, data):

        edit_ticket_window = tk.Toplevel()
        edit_ticket_window.geometry("600x300")
        edit_ticket_window.title("Edytuj Zgłoszenie")

        print(data)

        _id = data[0]
        _date = data[1]
        _client_name = data[2]
        _car_model = data[3]
        _year = data[4]
        _vin = data[5]
        _notes = data[6]

        main_frame = tk.Frame(edit_ticket_window)
        main_frame.pack(fill="both", padx=10, pady=5, expand=False)

        frame_left = tk.Frame(main_frame)
        frame_left.pack(side="left", padx=5, fill="both", expand=False)

        frame_left_label = tk.Frame(frame_left)
        frame_left_label.pack(side="left", fill="both", expand=False, padx=5, )
        frame_left_entry = tk.Frame(frame_left)
        frame_left_entry.pack(side="right", fill="both", expand=False)

        frame_right = tk.Frame(main_frame)
        frame_right.pack(side="right", padx=5, fill="both", expand=False)

        frame_right_label = tk.Frame(frame_right)
        frame_right_label.pack(side="left", fill="both", expand=False)
        frame_right_entry = tk.Frame(frame_right)
        frame_right_entry.pack(side="right", fill="both", expand=False)

        date_label = tk.Label(frame_left_label, text="Data zgłoszenia:")
        date_label.pack(padx=5, pady=5)
        date_entry = tk.Entry(frame_left_entry)
        date_entry.insert(0, _date)
        date_entry.pack(padx=5, pady=5)

        client_name_label = tk.Label(frame_left_label, text="Imię i nazwisko klienta:")
        client_name_label.pack(padx=5, pady=5)
        client_name_entry = tk.Entry(frame_left_entry)
        client_name_entry.insert(0, _client_name)
        client_name_entry.pack(padx=5, pady=5)

        car_model_label = tk.Label(frame_left_label, text="Model samochodu:")
        car_model_label.pack(padx=5, pady=5)
        car_model_entry = tk.Entry(frame_left_entry)
        car_model_entry.insert(0, _car_model)
        car_model_entry.pack(padx=5, pady=5)

        year_label = tk.Label(frame_left_label, text="Rok produkcji:")
        year_label.pack(padx=5, pady=5)
        year_entry = tk.Entry(frame_left_entry)
        year_entry.insert(0, _year)
        year_entry.pack(padx=5, pady=5)

        vin_label = tk.Label(frame_left_label, text="Numer VIN:")
        vin_label.pack(padx=5, pady=5)
        vin_entry = tk.Entry(frame_left_entry)
        vin_entry.insert(0, _vin)
        vin_entry.pack(padx=5, pady=5)

        notes_label = tk.Label(frame_right_label, text="Uwagi:")
        notes_label.pack(side=tk.TOP, padx=5, pady=5)
        notes_entry = tk.Text(frame_right_entry, width=20, height=10)
        notes_entry.insert(tk.END, _notes)
        notes_entry.pack(padx=5, pady=5, fill='both', expand=True)

        data_ = {
            "id": _id,
            "date": date_entry,
            "client_name": client_name_entry,
            "car_model": car_model_entry,
            "year": year_entry,
            "vin": vin_entry,
            "notes": notes_entry
        }

        frame_bottom = tk.Frame(edit_ticket_window)
        frame_bottom.pack(side=tk.BOTTOM, fill="both", padx=10, pady=5, expand=False)

        save_button = tk.Button(frame_bottom, text="Zapisz", command=lambda: update_entry(conn, c, data_, edit_ticket_window))
        save_button.pack(padx=5, pady=5)

        cancel_button = tk.Button(frame_bottom, text="Anuluj", command=edit_ticket_window.destroy)
        cancel_button.pack(padx=5, pady=5)

        edit_ticket_window.mainloop()

    def update_entry(self, conn, c, data, w):
        c.execute("UPDATE tickets SET date=?, client_name=?, car_model=?, year=?, vin=?, notes=? WHERE id=?",
                  (data["date"].get(),
                   data["client_name"].get(),
                   data["car_model"].get(),
                   data["year"].get(),
                   data["vin"].get(),
                   data["notes"].get('1.0', 'end-1c'),
                   data["id"]))
        conn.commit()
        w.destroy()
        display_data()


    def edit_entry(self, event):
        selected_item = tree.identify_row(event.y)
        conn = sqlite3.connect('service.db')
        c = conn.cursor()
        try:
            if selected_item:
                c.execute("SELECT * FROM tickets WHERE id=?", (selected_item,))
                ticket = c.fetchone()
                edit_window(conn, c, ticket)
        finally:
            conn.close()




    def quit_app(self):
        self.root.destroy()

    def menu_on_open_file(self):
        # Check if there is any connection to database
        global conn
        try:
            if conn:
                conn.close()
        except:
            pass

        options = {
            'defaultextension': '.db',
            'filetypes': [('Pliki bazy danych', '.db'), ('Wszystkie pliki', '.*')],
            'initialdir': 'C:\\',
            'initialfile': 'service.db',
            'title': 'Otwórz plik'
        }
        file = filedialog.askopenfile(mode='r', **options)
        if file is None:
            return

        # Copy current database to backup
        try:
            import shutil
            shutil.copy('service.db', 'service.db.bak')
        except Exception as e:
            show_popup('error', 'Błąd', 'Nie można wykonać kopii zapasowej bazy danych\n' + str(e))
            return

        # Copy file to new location
        try:
            shutil.copy(file.name, 'service.db')
        except Exception as e:
            show_popup('error', 'Błąd', 'Nie można otworzyć pliku\n' + str(e))
            return
        finally:
            file.close()

        display_data()
        show_popup('info', 'Informacja', 'Baza danych została załadowana')


    def menu_on_save_file(self):
        global conn
        try:
            if conn:
                conn.close()
        except:
            pass
        original_file = 'service.db'
        options = {
            'defaultextension': '.db',
            'filetypes': [('Pliki bazy danych', '.db'), ('Wszystkie pliki', '.*')],
            'initialdir': 'C:\\',
            'initialfile': 'service.db',
            'title': 'Zapisz plik'
        }
        file = filedialog.asksaveasfile(mode='w', **options)
        # Copy file to new location
        try:
            import shutil
            shutil.copy(original_file, file.name)
        except Exception as e:
            show_popup('error', 'Błąd', 'Nie można wyeksportować bazy danych\n' + str(e))
            return
        finally:
            file.close()

        show_popup('info', 'Informacja', 'Baza danych została wyeksportowana')


    def show_popup(self, _type, title, message):
        from tkinter import messagebox
        m = {
            "error": messagebox.showerror,
            "info": messagebox.showinfo,
            "warning": messagebox.showwarning
        }
        m[_type](title, message)


    def menu_on_exit(self):
        quit_app()


main = MainApplication()






