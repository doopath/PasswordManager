""" A list of constants for the PasswordManager."""

from pathlib import Path
import os


VERSION: str = "2.0"
APP_DIR: str = str(Path.home().joinpath("doopass"))

APPDATA_DIR: str = os.path.join(APP_DIR, "appdata")
DOOPASS_LOGO: str = """
______  _____  _____ ______   ___   _____  _____ 
|  _  \|  _  ||  _  || ___ \ / _ \ /  ___|/  ___|
| | | || | | || | | || |_/ // /_\ \\\\ `--. \ `--. 
| | | || | | || | | ||  __/ |  _  | `--. \ `--. \\
| |/ / \ \_/ /\ \_/ /| |    | | | |/\__/ //\__/ /
|___/   \___/  \___/ \_|    \_| |_/\____/ \____/ 
"""
HELP_LIST: str = "\n".join(
    [
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
        "##############################################################################################################",
    ]
)

STORE_BACKUP_EXTENSION: str = ".enc.bak"
STORE_FILE: str = os.path.join(APPDATA_DIR, "store.enc")
STORE_BACKUPS_DIR: str = os.path.join(APPDATA_DIR, "backups")
