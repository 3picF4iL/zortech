from database import Database
import os


class TestDataBase:
    def __init__(self, db="TestDataBase.db"):
        self.db = Database(db)
        self.clean_test = True
        self._create_test_data()

    def _create_test_data(self):
        assert self.db.create_table("test_table", "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER")
        assert self.db.add_entry("test_table", "name, age", "'John', 20")
        assert self.db.get_table_data("test_table") == [(1, 'John', 20)]

        assert self.db.get_table_data("test_table", "name") == [('John',)]

    def _clean_test_data(self):
        if self.db.check_if_table_exists("test_table"):
            self.db.delete_table("test_table")

    def _remove_test_database(self):
        os.remove(self.db.db)

    def test_create_table(self):
        self._clean_test_data()
        assert self.db.create_table("test_table", ("id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER"))
        assert self.db.check_if_table_exists("test_table")
        assert self.db.check_if_column_exists("test_table", "id")
        assert self.db.check_if_column_exists("test_table", "name")
        assert self.db.check_if_column_exists("test_table", "age")

    def test_edit_table(self):
        self._clean_test_data()
        assert self.db.create_table("test_table", "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER")
        assert self.db.edit_table("test_table", "phone TEXT")
        assert self.db.check_if_column_exists("test_table", "phone")

    def test_delete_table(self):
        self._clean_test_data()
        assert self.db.create_table("test_table", "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER")
        assert self.db.delete_table("test_table")
        assert not self.db.check_if_table_exists("test_table")

    def test_add_entry(self):
        self._clean_test_data()
        assert self.db.create_table("test_table", "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER")
        assert self.db.add_entry("test_table", "name, age", "'John', 20")
        assert self.db.get_table_data("test_table") == [(1, 'John', 20)]

    def test_edit_entry(self):
        self._clean_test_data()
        assert self.db.create_table("test_table", "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER")
        assert self.db.add_entry("test_table", "name, age", "'John', 20")
        assert self.db.edit_entry("test_table", "name='John'", "name='Anna'", "id=1")
        assert self.db.get_table_data("test_table") == [(1, 'Anna', 20)]

    def test_delete_entry(self):
        self._clean_test_data()
        assert self.db.create_table("test_table", "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER")
        assert self.db.add_entry("test_table", "name, age", "'John', 20")
        assert self.db.delete_entry("test_table", "name='John'")
        assert self.db.get_table_data("test_table") == []

    def _test_manager(self):
        for i, test in enumerate([t for t in dir(self) if t.startswith("test_")]):
            test_name = " ".join(test.split("_")[1:]).capitalize()
            print("{}. Test: \"{}\"...".format(i+1, test_name))
            getattr(self, test)()
            print("OK")

        print("=====================================")
        print("All tests passed")
        self._remove_test_database()

    def run_tests(self):
        self._test_manager()


if __name__ == "__main__":
    TestDataBase().run_tests()
