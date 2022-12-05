""" A list of constants for the PasswordManager. """

import sys

VERSION = "1.7"
APP_DIR = sys.path[0]
HELP_LIST = "\n".join([
    "##############################################################################################################",
    "#                                            PasswordManager  v1.7                                           #",
    "# Created by Doopath:                                                                                        #",
    "# Repository: https://github.com/doopath/PasswordManager                                                     #",
    "# List of the available options:                                                                             #",
    "# --init | -i                                                    | initialize a new store                    #",
    "# --get-value | -gv <prop name> <show/hide> <password?>          | get a value of a property                 #",
    "# --get-gh-token | -ggt <password?>                              | get your github token (shout be defined)  #",
    "# --set-value | -sv <name> <value> <password?>                   | set a value of a property                 #",
    "# --add-property | -ap <name> <value> <password?>                | add a <name> <value> pair to the store    #",
    "# --remove-property | -rp <name> <password?>                     | remove a <name>-value pair from the store #",
    "# --make-backup | -mb                                            | make a backup of the current store        #",
    "# --show-store | -ss <path?> <password?>                         | show a store on <path> or the current one #",
    "# --show-keys  | -sk <path?> <password?>                         | show keys of a store at <path> or the     #",
    "#                                                                | current one                               #",
    "##############################################################################################################"
])

STORE_FILE = f"{APP_DIR}/store.enc"
STORE_BACKUPS_DIR = f"{APP_DIR}/backups"
