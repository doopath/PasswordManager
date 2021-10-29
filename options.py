""" A list of options for the PasswordManager.  """

import base64
import datetime
from os import path
from os import mkdir
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from constants import STORE_FILE
from constants import STORE_BACKUPS_DIR


does_property_exist = lambda s, p: p in [ l.split("=")[0].strip() for l in s.split("\n") ]

def save_store(store: str, overwrite=False):
    """
    Save encrypted store on the disk.
    Usage:
        pass a store as a string.
    """

    if not path.isfile(STORE_FILE) and not overwrite:
        raise Exception("Store isn't initialized!")

    write_mode = "w+" if not overwrite else "w"

    with open(STORE_FILE, write_mode) as file:
        file.write(store)


def encrypt(key, source, encode=True):
    """
    Usage:
        pass a key (password) as a list of bytes,
        pass a source as an array of bytes.
    Return:
        encrypted data as a string if encode=True otherwise a list of bytes.
    """

    key = SHA256.new(key).digest()
    IV = Random.new().read(AES.block_size)
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    padding = AES.block_size - len(source) % AES.block_size
    source += bytes([padding]) * padding
    data = IV + encryptor.encrypt(source)

    return base64.b64encode(data).decode("latin-1") if encode else data


def decrypt(key, source, decode=True):
    """
    Usage:
        pass a key (password) as a list of bytes,
        pass a source (encrypted data) as a list of bytes.
    Return:
        decrypted data as a string.
    """

    if decode:
        source = base64.b64decode(source.encode("latin-1"))

    key = SHA256.new(key).digest()
    IV = source[:AES.block_size]
    decryptor = AES.new(key, AES.MODE_CBC, IV)
    data = decryptor.decrypt(source[AES.block_size:])
    padding = data[-1]

    if data[-padding:] != bytes([padding]) * padding:
        raise ValueError("Password is incorrect!")

    return data[:-padding].decode("utf-8")


def get_store(password=None, _decrypt=False, _path=STORE_FILE):
    """
    Usage:
        pass a password as a string (optional),
        set _decrypt=True if you want to get decrypted store (optional).
    Return:
        decrypted store as a string if the '_decrypt' flag is set,
        otherwise a list (encrypted!) of bytes.
    """

    with open(_path, "rb") as store:
        content = store.read().decode("utf-8")

        if _decrypt and password:
            password = password.encode("utf-8")
            content = decrypt(password, content).strip("\n").split("\n")
            content = "\n".join(set([ l.strip() for l in content ]))

        return content


def get_value(name: str, password: str):
    """
    Usage:
        pass a name of a property as a string (name of a property in the store),
        pass a password as a string.
    Return:
        a value of the property
    """

    store_content = get_store(password, True)
    store_content = store_content.split("\n")
    value = None

    for line in store_content:
        items = line.split("=")

        if items[0].strip() == name:
            value = items[1].strip()

    if value is None:
        raise ValueError(f"The property '{name}' is not set in the store!")

    return value


def add_property(name: str, value: str, password: str):
    """
    Add a property to the store.
    Usage:
        pass a name of the property as a string,
        pass a value of the property as a string,
        pass a password for store decryption and encryption.
    """

    store = get_store(password, _decrypt=True)

    if does_property_exist(store, name):
        raise Exception(f"This property ({name}) already exists!")

    store += f"\n{name} = {value}"
    store = encrypt(password.encode("utf-8"), store.encode("utf-8"))

    save_store(store)


def modify_property(name: str, password: str, f):
    store = get_store(password, _decrypt=True)

    if not does_property_exist(store, name):
        raise Exception(f"The property ({name}) does not exist!")

    store = [ l for l in store.split("\n") ]

    for line in store:
        items = [ x.strip() for x in line.split("=") ]

        if items[0] == name:
            f(store, line)

    store = "\n".join(store)
    store = encrypt(password.encode("utf-8"), store.encode("utf-8"))

def remove_property(name: str, password: str):
    """
    Remove a set property from the store.
    Usage:
        pass a name of property to remove as a string,
        pass a password as a string.
    """
    f = lambda s, l: s.remove(s.index(l))
    modify_property(name, password, f)


def set_value(name: str, value: str, password: str):
    """
    Set a value of a property in the store.
    Usage:
        pass a name of a property as a string,
        pass a value of the property as a string,
        pass a password as a string.
    """

    def f(s, l): s[s.index(l)] = f"{name} = {value}"
    modify_property(name, password, f)


def make_store_backup():
    """
    Make a backup of the current store.
    New backup will be saved on <app_dir>/backups/
    """

    date = datetime.date.today()
    current_date = date.strftime("%d_%m_%Y")
    store_name = STORE_FILE.split("/")[-1]
    backup_name = f"{str(current_date)}_{store_name}"
    store = get_store()

    if not path.isdir(STORE_BACKUPS_DIR):
        mkdir(STORE_BACKUPS_DIR)

    with open(f"{STORE_BACKUPS_DIR}/{backup_name}", "w+") as backup:
        backup.write(store)


def show_store(password: str, store_path=STORE_FILE):
    """
    Show decrypted store.
    Usage:
        pass a password as a string,
        pass a store location as a string (optional).
    """

    if not path.isfile(store_path):
        raise Exception("File on path={store_path} does not exist!")

    store = get_store(password, _decrypt=True, _path=store_path)

    if store.strip().strip("\n") == "":
        store =  "*The store is empty (see --help)*"

    print("\n#########################################")
    print("Your passwords (shown as <name = value>):\n")
    print(store)
    print("\n#########################################\n")


def initialize_store(password: str):
    """
    Initialze a new store.
    """

    if path.isfile(STORE_FILE):
        answ = input("The store already had been initialized, overwrite? (y/n): ")
        if answ.lower() == "n": return
        elif answ.lower() != "y":
            print("The store was successfully initialized!")
            initialize_store(password)

    save_store(encrypt(password.encode("utf-8"), "".encode("utf-8")), overwrite=True)

