""" A list of constants for the PasswordManager.
    Be sure you import the whole module instead of a single constant,
    because the update() function may be used by other modules and the
    paths could be changed.
"""

VERSION: str = "2.0"
APP_DIR = ""

APPDATA_DIR: str = f"{APP_DIR}/appdata"
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
STORE_FILE: str = f"{APPDATA_DIR}/store.enc"
STORE_BACKUPS_DIR: str = f"{APPDATA_DIR}/backups"


def update(projectRoot: str):
    global APP_DIR, APPDATA_DIR, STORE_FILE, STORE_BACKUPS_DIR
    APP_DIR = projectRoot
    APPDATA_DIR = f"{APP_DIR}/appdata"
    STORE_FILE = f"{APPDATA_DIR}/store.enc"
    STORE_BACKUPS_DIR = f"{APPDATA_DIR}/backups"
