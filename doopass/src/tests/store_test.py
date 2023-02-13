""" Tests of the 'options' module. """

import unittest
import os
import shutil
from src.core.store import Store
from src.core import constants
from src.core.exceptions import PropertyDoesNotExistError
from src.core.exceptions import IncorrectPasswordError


class StoreTest(unittest.TestCase):
    def setUp(self):
        self.prop_name = "aProp"
        self.prop_value = "aValue"
        self.password = "aPassword"
        self.store_path = constants.STORE_FILE
        self.backup_path = constants.STORE_BACKUPS_DIR
        self._clear_appdata()
        self.store = Store(self.password)

    def _clear_appdata(self):
        appdata_dir = constants.APPDATA_DIR
        if os.path.isdir(appdata_dir):
            shutil.rmtree(appdata_dir)

    def _get_file_content(self, path: str) -> str:
        with open(path, "r") as file:
            return str(file.read())

    def test_initialize_store(self):
        assert os.path.isfile(
            self.store_path
        ), "The 'initialize_store' function should create a store!"

    def test_add_property_get_value(self):
        self.store.add_property(self.prop_name, self.prop_value)
        value = self.store.get_value(self.prop_name)

        is_value_right = self.prop_value == value

        assert is_value_right, "The added property should have correct value!"

    def test_set_value(self):
        self.store.add_property(self.prop_name, self.prop_value)
        new_value = "newValue"
        self.store.set_value(self.prop_name, new_value)
        value = self.store.get_value(self.prop_name)

        is_value_right = value == new_value

        assert is_value_right, "The set property should have correct value!"

    def test_remove_property(self):
        self.store.add_property(self.prop_name, self.prop_value)
        self.store.remove_property(self.prop_name)

        is_removed = False

        try:
            self.store.get_value(self.prop_name)
        except PropertyDoesNotExistError:
            is_removed = True

        assert is_removed, "The 'remove_property' function should remove the property!"

    def test_get_store(self):
        store = self.store.get_store(_decrypt=True)

        is_store_correct = store == ""

        self.store.add_property(self.prop_name, self.prop_value)
        store = self.store.get_store(_decrypt=True)

        is_store_correct &= store == f"{self.prop_name} = {self.prop_value}"

        assert is_store_correct, "The gotten store isn't correct!"

    def test_encrypt_decrypt(self):
        key = self.password.encode("utf-8")
        source = self.prop_value
        encrypted_source = self.store.encrypt(source.encode("utf-8")).encode("utf-8")
        decrypted_source = self.store.decrypt(key, encrypted_source)
        is_everything_right = decrypted_source == source

        assert is_everything_right, "Decrypted data doesn't equal the initial one!"

    def test_incorrect_password(self):
        is_everything_right = False

        try:
            self.store = Store("incorrectPassword")
        except IncorrectPasswordError:
            is_everything_right = True

        assert is_everything_right, (
            "The 'get_store' function should raise the IncorrectPasswordError"
            + " if the given password isn't correct!"
        )


def test():
    unittest.main()


if __name__ == "__main__":
    test()
