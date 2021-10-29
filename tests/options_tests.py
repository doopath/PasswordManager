""" Tests of the 'options' module. """

import unittest
import os
import sys
import datetime
from core import options
from core import constants
from core.exceptions import PropertyDoesNotExistError


class OptionsTest(unittest.TestCase):
    def setUp(self):
        self.prop_name = "aProp"
        self.prop_value = "aValue"
        self.password = "aPassword"
        self.work_dir = sys.path[0]
        self.store_path = constants.STORE_FILE
        self.backup_path = f"{self.work_dir}/backups"
        self._remove_store_if_exists()
        self._remove_backup_if_exists()
        options.initialize_store(self.password)


    def tearDown(self):
        self.prop_name = None
        self.prop_value = None
        self.password = None
        self.work_dir = None
        self.store_path = None


    def _remove_if_exists(self, path: str):
        if os.path.isfile(path):
            os.remove(path)

    def _remove_store_if_exists(self):
        self._remove_if_exists(self.store_path)

    def _remove_backup_if_exists(self):
        self._remove_if_exists(self.backup_path)


    def _get_file_content(self, path: str):
        with open(path, "r") as file:
            return file.read()


    def test_initialize_store(self):
        assert os.path.isfile(self.store_path),\
                "The 'initialize_store' function should create a store!"


    def test_make_store_backup(self):
        options.make_store_backup()
        date = datetime.date.today().strftime("/%d_%m_%Y_")
        backup_file_path = self.backup_path + date + self.store_path.split("/")[-1]

        is_backup_right = os.path.isdir(self.backup_path)
        is_backup_right = is_backup_right and os.path.isfile(backup_file_path)
        is_backup_right = (is_backup_right and
            self._get_file_content(backup_file_path) == self._get_file_content(self.store_path))

        assert is_backup_right,\
            "The 'make_store_backup' function should create a backup of current store!"


    def test_add_property_get_value(self):
        options.add_property(self.prop_name, self.prop_value, self.password)
        value = options.get_value(self.prop_name, self.password)

        is_value_right = self.prop_value == value

        assert is_value_right, "The added property should have correct value!"


    def test_set_value(self):
        options.add_property(self.prop_name, self.prop_value, self.password)
        new_value = "newValue"
        options.set_value(self.prop_name, new_value, self.password)
        value = options.get_value(self.prop_name, self.password)

        is_value_right = value == new_value

        assert is_value_right, "The set property should have correct value!"

    def test_remove_property(self):
        options.add_property(self.prop_name, self.prop_value, self.password)
        options.remove_property(self.prop_name, self.password)

        is_removed = False

        try:
            options.get_value(self.prop_name, self.password)
        except PropertyDoesNotExistError:
            is_removed = True

        assert is_removed, "The 'remove_property' function should remove the property!"


    def test_get_store(self):
        store = options.get_store(self.password, _decrypt=True)

        is_store_correct = store == ""

        options.add_property(self.prop_name, self.prop_value, self.password)
        store = options.get_store(self.password, _decrypt=True)

        is_store_correct = is_store_correct and store == f"{self.prop_name} = {self.prop_value}"

        assert is_store_correct, "The gotten store isn't correct!"


    def test_encrypt_decrypt(self):
        key = self.password.encode("utf-8")
        source = self.prop_value
        encryted_source = options.encrypt(key, source.encode("utf-8"))
        decrypted_source = options.decrypt(key, encryted_source)

        is_everything_right = decrypted_source == source

        assert is_everything_right, "Decrypted data doesn't equal the initial one!"


    def test_save_get_store(self):
        options.add_property(self.prop_name, self.prop_value, self.password)
        new_store_value = ""
        new_store = options.encrypt(self.password.encode("utf-8"), new_store_value.encode("utf-8"))
        options.save_store(new_store, overwrite=True)
        store = options.get_store(self.password, _decrypt=True)

        is_store_correct = store == new_store_value

        assert is_store_correct, "The 'save_store' functions should change the store value!"\
            " And the 'get_store' one should returns it correctly!"


def test():
    unittest.main()


(lambda: test() if __name__ == "__main__" else None)()

