""" A list of option aliases. """

from getpass import getpass
import pyperclip
from core import options
from core.constants import HELP_LIST
from core.constants import VERSION


def get_password(args, i: int):
    if len(args) == i+1:
        return args[i]

    return getpass("Password for the store: ")


def get_value(args):
    name = args[0]
    password = get_password(args, 1)
    value = options.get_value(name, password)
    pyperclip.copy(value)

    print("\nValue: " + value)
    print("*Copied to the clipboard*")


def show_store(args):
    password = get_password(args, 1)

    if len(args) == 2:
        options.show_store(password, store_path=args[1])
    else: options.show_store(password)


def get_gh_token(args):
    get_value(["github-token"] + args)


def set_value(args):
    name = args[0]
    value = args[1]
    password = get_password(args, 2)
    options.set_value(name, value, password)

    print("\nProperty was successfully set!")


def add_property(args):
    name = args[0]
    value = args[1]
    password = get_password(args, 2)
    options.add_property(name, value, password)

    print("\nProperty was successfully added!")


def remove_property(args):
    name = args[0]
    password = get_password(args, 1)
    options.remove_property(name, password)

    print("\nProperty was successfully removed!")


def make_store_backup(_):
    options.make_store_backup()


def show_help_list(_):
    print(HELP_LIST)


def show_version(_):
    print(f"\nPasswordManager v{VERSION}")


def initialize_store(args):
    password1 = getpass("Enter a passwrod for a new store: ")
    password2 = getpass("Repeat the passwrod: ")

    if password1 != password2:
        print("The password doesn't match!\n")
        initialize_store(args)
        return

    options.initialize_store(password1)
    print("\nThe store was successfully initialized!")

