""" A list of constants for the PasswordManager. """

import sys

VERSION = "1.3"
HELP_LIST = "\n".join([
    "##################################################################################################",
    "#                                      PasswordManager  v1.3                                     #",
    "# Created by Doopath:                                                                            #",
    "# Repo: https://github.com/doopath/PasswordManager                                               #",
    "# List of availabe options:                                                                      #",
    "# --get-value | -gv <prop name> <password?>          | get a value of a property                 #",
    "# --get-gh-token | -ggh <password?>                  | get your github token (shout be defined)  #",
    "# --set-value | -sv <name> <value> <password?>       | set a value of a property                 #",
    "# --add-property | -ap <name> <value> <password?>    | add a <name> <value> pair to the store    #",
    "# --remove-property | -rp <name> <value> <password?> | add a <name> <value> pair to the store    #",
    "# --make-backup | -mb <password?>                    | make a backup of the current store        #",
    "# --show-store | -ss <path?> <password?>             | show a store on <path> or the current one #",
    "##################################################################################################"
])

STORE_FILE = f"{sys.path[0]}/store.enc"
STORE_BACKUPS_DIR = f"{sys.path[0]}/backups"
