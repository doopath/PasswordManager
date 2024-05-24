""" A list of constants for the PasswordManager."""

from pathlib import Path
import os


VERSION: str = "2.3"
APP_DIR: str = str(Path.home().joinpath("doopass"))
APPDATA_DIR: str = os.path.join(APP_DIR, "appdata")
STORE_BACKUP_EXTENSION: str = ".enc.bak"
STORE_FILE: str = os.path.join(APPDATA_DIR, "store.enc")
LOG_FILE: str = os.path.join(APPDATA_DIR, "doopass.log")
STORE_BACKUPS_DIR: str = os.path.join(APPDATA_DIR, "backups")
DOOPASS_LOGO: str = """
______  _____  _____ ______   ___   _____  _____ 
|  _  \|  _  ||  _  || ___ \ / _ \ /  ___|/  ___|
| | | || | | || | | || |_/ // /_\ \\\\ `--. \ `--. 
| | | || | | || | | ||  __/ |  _  | `--. \ `--. \\
| |/ / \ \_/ /\ \_/ /| |    | | | |/\__/ //\__/ /
|___/   \___/  \___/ \_|    \_| |_/\____/ \____/ 
"""
