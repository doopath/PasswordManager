""" A list of constants for the PasswordManager. """

import sys

VERSION = "1.0"
HELP_LIST = "\n".join([
    "#################################################################################",
    "#                              PasswordManager  v1.0                            #",
    "# Created by Doopath:                                                           #",
    "# Repo: https://github.com/doopath/PasswordManager                              #",
    "# List of availabe options:                                                     #",
    "# --get-value <prop name>          | get a value of a property                  #",
    "# --get-gh-token                   | get your github token (shout be defined)   #",
    "# --set-value <name> <value>       | set a value of a property                  #",
    "# --add-property <name> <value>    | add a <name> <value> pair to the store     #",
    "# --make-backup                    | make a backup of the current store         #",
    "# --show-store <path?>             | show a store on <path> or the current one  #",
    "#################################################################################"
])

STORE_FILE = f"{sys.path[0]}/store.enc"
STORE_BACKUPS_DIR = f"{sys.path[0]}/backups"
