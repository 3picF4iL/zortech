from misc import Entity


class _Object(Entity):
    def __init__(self, data, db):
        super().__init__()
        self._id = None
        self.data = data
        self.database = db
        self.setup_values()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not self._id:
            self._id = value

    def get_id(self):
        if self._id is None:
            self._id = self.exists()
        return self._id

    def _setattr(self, name, value):
        if hasattr(self, name):
            if isinstance(name, list):
                name.append(value)
            else:
                setattr(self, name, value)

    def setup_values(self):
        print(self.data.items)
        for key, value in self.data.items():
            self._setattr(key, value)

    def gen_data(self):
        raise NotImplemented

    def add(self):
        raise NotImplemented

    def update(self):
        raise NotImplemented

    def exists(self):
        raise NotImplemented


class Car(_Object):
    def __init__(self, data, db):
        self.customer_id = None
        self.brand_id = None
        self.model_id = None
        self.color_id = None
        self.year = None
        self.vin = None
        super().__init__(data, db)

    def gen_data(self):
        return {
            'customer_id': self.customer_id,
            'brand_id': self.brand_id,
            'model_id': self.model_id,
            'color_id': self.color_id,
            'year': self.year,
            'vin': self.vin
        }

    def add(self):
        if not self.get_id():
            self._id = self.database.add_item_to_table('cars', self.gen_data())
            self.logger.debug(f"Car not in database, added with ID: {self._id}")
        return self._id

    def exists(self):
        # TODO: We need to check more fields e.g. year
        data = {
            'customer_id': self.customer_id,
            'brand_id': self.brand_id
        }
        car_id = self.database.check_if_car_exists(data)
        if car_id:
            self.logger.debug(f"Car exists in database with ID: {car_id}")
        return car_id

    def update(self):
        data = self.gen_data()
        data['id'] = self.id
        self.database.update_car(data)


class Model(_Object):
    def __init__(self, data, db):
        self.brand_id = None
        self.name = None
        super().__init__(data, db)


class Brand(_Object):
    def __init__(self, data, db):
        self.name = None
        super().__init__(data, db)


class Color(_Object):
    def __init__(self, data, db):
        self.name = None
        super().__init__(data, db)

    def exists(self):
        color_id = self.database.get_item_from_name('colors', self.name)
        return color_id


class Customer(_Object):
    def __init__(self, data, db):
        self.first_name = None
        self.last_name = None
        self.phone = None
        self.email = None
        self.cars = []
        super().__init__(data, db)

    def gen_data(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'email': self.email
        }

    def add(self):
        if not self.get_id():
            self._id = self.database.add_item_to_table('customers', self.gen_data())
            self.logger.debug(f"Customer not in database, added with ID: {self._id}")
        return self._id

    def exists(self):
        data = {
            'last_name': self.last_name,
            'phone': self.phone
        }
        customer_id = self.database.check_if_customer_exists(data)
        if customer_id:
            self.logger.debug(f"Customer exists in database with id: {customer_id}")
        return customer_id

    def update(self):
        data = self.gen_data()
        data['id'] = self.id
        self.database.update_customer(data)


class Ticket(_Object):
    def __init__(self, data, db):
        self.customer_id = None
        self.car_id = None
        self.date_creation = None
        self.date_modification = None
        self.notes = None
        super().__init__(data, db)

    def gen_data(self):
        return {
            'customer_id': self.customer_id,
            'car_id': self.car_id,
            'date_creation': self.date_creation,
            'date_modification': self.date_modification,
            'notes': self.notes
        }

    def add(self):
        self._id = self.database.add_item_to_table('tickets', self.gen_data())
        return self._id

    def update(self):
        data = self.gen_data()
        data['id'] = self.id
        self.database.update_ticket(data)


class TicketDAO(Entity):
    def __init__(self, data, db):
        super().__init__()
        self._id = None
        self.database = db
        self.id = data.get('id')
        self.date_creation = data.get('date_creation')
        self.date_modification = data.get('date_modification')
        self.customer_id = data.get('customer_id')
        self.car_id = data.get('car_id')
        self.notes = data.get('notes')

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not self._id and value:
            self._id = value


class CustomerDAO(Entity):
    def __init__(self, data, db):
        super().__init__()
        self._id = None
        self.database = db
        self.id = data.get('customer_id')
        self.car_id = data.get('car_id')
        self.collected_data = None
        self.load_data()

    def load_data(self):
        self.collected_data = self.database.get_item_from_id('customers', self._id)

    def print_data(self):
        print(self.collected_data)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not self._id and value:
            self._id = value


class CarDAO(Entity):
    def __init__(self, data, db):
        super().__init__()
        self._id = None
        self.database = db
        self.id = data.get('car_id')
        self.collected_data = None
        self.load_data()

    def load_data(self):
        self.collected_data = self.database.get_item_from_id('cars', self._id)

    def print_data(self):
        print(self.collected_data)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not self._id and value:
            self._id = value
