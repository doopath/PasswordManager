""" Module that describes the store logic. """

import datetime
import secrets
import os
from base64 import urlsafe_b64decode as b64d
from base64 import urlsafe_b64encode as b64e
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from .constants import STORE_BACKUPS_DIR, STORE_FILE, APPDATA_DIR
from .exceptions import (
    IncorrectPasswordError,
    PropertyAlreadyExistError,
    PropertyDoesNotExistError,
    StoreIsNotInitializedError,
)


class Store:
    ITERATIONS = 100_000

    def __init__(self, password: str):
        self.backend = default_backend()
        self.password = password
        self._initialize_store_file()
        self.decrypted_store = str(self.get_store(_decrypt=True))

    def _derive_key(
        self, password: bytes, salt: bytes, iterations: int = ITERATIONS
    ) -> bytes:
        """Derive a secret key from a given password and salt"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=iterations,
            backend=self.backend,
        )
        return b64e(kdf.derive(password))

    def does_property_exist(self, prop: str) -> bool:
        return prop in [
            line.split("=")[0].strip() for line in self.decrypted_store.split("\n")
        ]

    def _initialize_backups_dir(self) -> None:
        """
        Initialize a directory for the backups.
        """

        if not os.path.isdir(STORE_BACKUPS_DIR):
            os.mkdir(STORE_BACKUPS_DIR)

    def _initialize_appdata_dir(self) -> None:
        """
        Initialize a directory for the application data.
        """

        if not os.path.isdir(APPDATA_DIR):
            os.mkdir(APPDATA_DIR)

    def _initialize_store_file(self) -> None:
        """
        Initialize a store file if it doesn't exist.
        """

        self._initialize_appdata_dir()

        if not does_store_file_exist():
            with open(STORE_FILE, "w") as file:
                file.write(self.encrypt(bytes()))

    def save_store(self, overwrite=False) -> None:
        """
        Save encrypted store on the disk.
        Usage:
            pass a store as a string.
        """

        if not os.path.isfile(STORE_FILE) and not overwrite:
            raise StoreIsNotInitializedError("Store isn't initialized!")

        write_mode = "w+" if not overwrite else "w"

        with open(STORE_FILE, write_mode) as file:
            file.write(self.encrypt(self.decrypted_store.encode("utf-8")))

    def encrypt(self, source: bytes, iterations: int = ITERATIONS) -> str:
        """
        Usage:
            pass a key (password) as a list of bytes,
            pass a source as a list of bytes.
        Returns:
            encrypted source as a list of bytes.
        """

        salt = secrets.token_bytes(16)
        key = self._derive_key(self.password.encode("utf-8"), salt, iterations)
        return b64e(
            b"%b%b%b"
            % (
                salt,
                iterations.to_bytes(4, "big"),
                b64d(Fernet(key).encrypt(source)),
            )
        ).decode()

    def decrypt(self, key: bytes, source: bytes) -> str:
        """
        Usage:
            pass a key (password) as a list of bytes,
            pass a source (encrypted data) as a list of bytes.
        Return:
            decrypted data as a string.
        """

        decoded = b64d(source)
        salt, itr, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
        iterations = int.from_bytes(itr, "big")
        key = self._derive_key(key, salt, iterations)

        try:
            return Fernet(key).decrypt(token).decode()
        except InvalidToken:
            raise IncorrectPasswordError("Password is incorrect!")

    def get_store(self, _decrypt: bool = False, _path: str = STORE_FILE) -> str | bytes:
        """
        Usage:
            set _decrypt=True if you want to get decrypted store (optional).
        Return:
            decrypted store as a string if the '_decrypt' flag is set,
            otherwise a list (encrypted!) of bytes.
        """

        with open(_path, "rb") as store:
            content = store.read()
            decrypted_content = None
            result = None

            if _decrypt:
                user_password: bytes = self.password.encode("utf-8")
                decrypted_content = (
                    self.decrypt(user_password, content).strip("\n").split("\n")
                )

                result = "\n".join(set([l.strip() for l in decrypted_content]))

            return result if result is not None else content

    def get_value(self, name: str) -> str:
        """
        Usage:
            pass a name of a property as a string (name of a property in the store),
        Return:
            a value of the property
        """

        content = self.decrypted_store.split("\n")
        value = None

        for line in content:
            items = line.split("=")

            if items[0].strip() == name:
                value = items[1].strip()

        if value is None:
            raise PropertyDoesNotExistError(
                f"The property '{name}' is not set in the store!"
            )

        return value

    def add_property(self, name: str, value: str) -> None:
        """
        Add a property to the store.
        Usage:
            pass a name of the property as a string,
            pass a value of the property as a string,
        """

        if self.does_property_exist(name):
            raise PropertyAlreadyExistError(f"This property ({name}) already exists!")

        self.decrypted_store += f"\n{name} = {value}"
        self.save_store()

    def modify_property(self, name: str, f) -> None:
        if not self.does_property_exist(name):
            raise PropertyDoesNotExistError(f"The property ({name}) does not exist!")

        store = [l for l in self.decrypted_store.split("\n")]

        for line in store:
            items = [x.strip() for x in line.split("=")]

            if items[0] == name:
                f(store, line)

        self.decrypted_store = "\n".join(store)
        self.save_store()

    def remove_property(self, name: str) -> None:
        """
        Remove a set property from the store.
        Usage:
            pass a name of property to remove as a string,
        """

        def f(s, l):
            if l not in s:
                raise PropertyDoesNotExistError(
                    f"The property ({name}) does not exist!"
                )
            s.pop(s.index(l))

        self.modify_property(name, f)

    def set_value(self, name: str, value: str) -> None:
        """
        Set a value of a property in the store.
        Usage:
            pass a name of a property as a string,
            pass a value of the property as a string,
        """

        def f(s, l):
            s[s.index(l)] = f"{name} = {value}"

        self.modify_property(name, f)

    def get_keys(self) -> list[str]:
        """
        Return:
            a list of all keys in the store.
        """

        return [l.split("=")[0].strip() for l in self.decrypted_store.split("\n")]

    def make_store_backup(self) -> None:
        """
        Make a backup of the current store.
        New backup will be saved on <app_dir>/backups/
        """

        date = datetime.date.today()
        current_date = date.strftime("%d_%m_%Y")
        store_name = STORE_FILE.split("/")[-1]
        backup_name = f"{str(current_date)}_{store_name}"
        store = self.encrypt(self.decrypted_store.encode("utf-8"))

        self._initialize_backups_dir()

        with open(f"{STORE_BACKUPS_DIR}/{backup_name}", "w+") as backup:
            backup.write(store)


def try_initialize_store(password: str) -> Store | None:
    try:
        return Store(password)
    except IncorrectPasswordError:
        return None


def try_initialize_existing_store(password: str) -> Store | None:
    if os.path.isdir(APPDATA_DIR) and os.path.isfile(STORE_FILE):
        return try_initialize_store(password)
    else:
        raise StoreIsNotInitializedError("Store isn't initialized!")


def does_store_file_exist() -> bool:
    return os.path.isdir(APPDATA_DIR) and os.path.isfile(STORE_FILE)
