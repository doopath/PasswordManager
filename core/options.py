""" A list of options for the PasswordManager.  """

import datetime
import secrets
from typing import Optional
from base64 import urlsafe_b64decode as b64d
from base64 import urlsafe_b64encode as b64e
from os import mkdir, path

from cryptography.fernet import (Fernet, InvalidToken)
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from core.constants import STORE_BACKUPS_DIR, STORE_FILE
from core.exceptions import (IncorrectPasswordError, PropertyAlreadyExistError,
                             PropertyDoesNotExistError,
                             StoreIsNotInitializedError)


BACKEND = default_backend()
ITERATIONS = 100_000


def does_property_exist(store: str, prop: str) -> bool:
    return prop in [line.split("=")[0].strip() for line in store.split("\n")]


def _derive_key(password: bytes, salt: bytes, iterations: int = ITERATIONS) -> bytes:
    """Derive a secret key from a given password and salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt,
        iterations=iterations, backend=BACKEND)
    return b64e(kdf.derive(password))


def save_store(store: str, overwrite=False) -> None:
    """
    Save encrypted store on the disk.
    Usage:
        pass a store as a string.
    """

    if not path.isfile(STORE_FILE) and not overwrite:
        raise StoreIsNotInitializedError("Store isn't initialized!")

    write_mode = "w+" if not overwrite else "w"

    with open(STORE_FILE, write_mode) as file:
        file.write(store)


def encrypt(key: bytes, source: bytes, iterations: int = ITERATIONS) -> str:
    """
    Usage:
        pass a key (password) as a list of bytes,
        pass a source as a list of bytes.
    Returns:
        encrypted source as a list of bytes.
    """

    salt = secrets.token_bytes(16)
    key = _derive_key(key, salt, iterations)
    return b64e(
        b'%b%b%b' % (
            salt,
            iterations.to_bytes(4, 'big'),
            b64d(Fernet(key).encrypt(source)),
        )
    ).decode()


def decrypt(key: bytes, source: bytes) -> str:
    """
    Usage:
        pass a key (password) as a list of bytes,
        pass a source (encrypted data) as a list of bytes.
    Return:
        decrypted data as a string.
    """

    decoded = b64d(source)
    salt, itr, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
    iterations = int.from_bytes(itr, 'big')
    key = _derive_key(key, salt, iterations)

    try:
        return Fernet(key).decrypt(token).decode()
    except InvalidToken:
        raise IncorrectPasswordError("Password is incorrect!")


def get_store(password: str = None, _decrypt: bool = False, _path: str = STORE_FILE) -> str | bytes:
    """
    Usage:
        pass a password as a string (optional),
        set _decrypt=True if you want to get decrypted store (optional).
    Return:
        decrypted store as a string if the '_decrypt' flag is set,
        otherwise a list (encrypted!) of bytes.
    """

    with open(_path, "rb") as store:
        content = store.read()

        if _decrypt and password:
            user_password: bytes = password.encode("utf-8")
            content = decrypt(user_password, content).strip("\n").split("\n")
            content = "\n".join(set([l.strip() for l in content]))

        return content


def get_value(name: str, password: str) -> str:
    """
    Usage:
        pass a name of a property as a string (name of a property in the store),
        pass a password as a string.
    Return:
        a value of the property
    """

    store_content = str(get_store(password, _decrypt=True))
    content = store_content.split("\n")
    value = None

    for line in content:
        items = line.split("=")

        if items[0].strip() == name:
            value = items[1].strip()

    if value is None:
        raise PropertyDoesNotExistError(
            f"The property '{name}' is not set in the store!")

    return value


def add_property(name: str, value: str, password: str) -> None:
    """
    Add a property to the store.
    Usage:
        pass a name of the property as a string,
        pass a value of the property as a string,
        pass a password for store decryption and encryption.
    """

    store = str(get_store(password, _decrypt=True))

    if does_property_exist(store, name):
        raise PropertyAlreadyExistError(
            f"This property ({name}) already exists!")

    store += f"\n{name} = {value}"
    store = encrypt(password.encode("utf-8"), store.encode("utf-8"))

    save_store(store)


def modify_property(name: str, password: str, f) -> None:
    store = str(get_store(password, _decrypt=True))

    if not does_property_exist(store, name):
        raise PropertyDoesNotExistError(
            f"The property ({name}) does not exist!")

    store = [l for l in store.split("\n")]

    for line in store:
        items = [x.strip() for x in line.split("=")]

        if items[0] == name:
            f(store, line)

    store = "\n".join(store)
    store = encrypt(password.encode("utf-8"), store.encode("utf-8"))

    save_store(store)


def remove_property(name: str, password: str) -> None:
    """
    Remove a set property from the store.
    Usage:
        pass a name of property to remove as a string,
        pass a password as a string.
    """

    def f(s, l):
        if l not in s:
            raise PropertyDoesNotExistError(
                f"The property ({name}) does not exist!")
        s.pop(s.index(l))

    modify_property(name, password, f)


def set_value(name: str, value: str, password: str) -> None:
    """
    Set a value of a property in the store.
    Usage:
        pass a name of a property as a string,
        pass a value of the property as a string,
        pass a password as a string.
    """

    def f(s, l): s[s.index(l)] = f"{name} = {value}"

    modify_property(name, password, f)


def make_store_backup() -> None:
    """
    Make a backup of the current store.
    New backup will be saved on <app_dir>/backups/
    """

    date = datetime.date.today()
    current_date = date.strftime("%d_%m_%Y")
    store_name = STORE_FILE.split("/")[-1]
    backup_name = f"{str(current_date)}_{store_name}"
    guess_store = get_store()
    store: bytes = guess_store if type(guess_store) is bytes else bytes()

    if not path.isdir(STORE_BACKUPS_DIR):
        mkdir(STORE_BACKUPS_DIR)

    with open(f"{STORE_BACKUPS_DIR}/{backup_name}", "w+") as backup:
        backup.write(store.decode())


def show_store(password: str, store_path: str = STORE_FILE) -> None:
    """
    Show decrypted store.
    Usage:
        pass a password as a string,
        pass a store location as a string (optional).
    """

    if not path.isfile(store_path):
        raise Exception("File on path={store_path} does not exist!")

    store = str(get_store(password, _decrypt=True, _path=store_path))

    if store.strip().strip("\n") == "":
        store = "*The store is empty (see --help)*"

    print("\n#########################################")
    print("Your passwords (shown as <name = value>):\n")
    print(store)
    print("\n#########################################\n")


def initialize_store(password: str) -> bool:
    """
    Initialize a new store.
    """

    if path.isfile(STORE_FILE):
        answ = input(
            "The store already had been initialized, overwrite? (y/n): ").lower()
        if answ == "n":
            return False
        elif answ == "y":
            save_store(encrypt(password.encode("utf-8"),
                               "".encode("utf-8")), overwrite=True)
            return True
        else:
            return initialize_store(password)

    else:
        save_store(encrypt(password.encode("utf-8"),
                           "".encode("utf-8")), overwrite=True)
        return True
