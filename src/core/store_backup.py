import os
from typing import List
from . import constants
from datetime import datetime


class StoreBackup:
    def __init__(self) -> None:
        self._initialize_backup_dir()

    def _initialize_backup_dir(self) -> None:
        if not os.path.isdir(constants.APPDATA_DIR):
            os.mkdir(constants.APPDATA_DIR)

        if not os.path.isdir(constants.STORE_BACKUPS_DIR):
            os.mkdir(constants.STORE_BACKUPS_DIR)

    def _get_file_content(self, filepath: str) -> str:
        content = ""

        with open(filepath, "r") as store:
            content = store.read()

        return content

    def _get_dated_backups(self, base: str) -> List[str]:
        backups = os.listdir(constants.STORE_BACKUPS_DIR)
        dated_backups = [
            b for b in backups if b.startswith(base) and b.endswith(".enc.bak")
        ]

        return sorted(dated_backups)

    def get_store_content(self) -> str:
        return self._get_file_content(constants.STORE_FILE)

    def get_backup_content(self, backup_name: str) -> str:
        backup_path = os.path.join(constants.STORE_BACKUPS_DIR, backup_name)
        return self._get_file_content(backup_path)

    def make_backup(self) -> None:
        date = datetime.date.today()
        current_date = date.strftime("%d_%m_%Y")
        store_name = constants.STORE_FILE.split("/")[-1]
        backup_name = f"{str(current_date)}_{store_name}"
        store_content = self.get_store_content()
        backup_path = os.path.join(constants.STORE_BACKUPS_DIR, backup_name)
        backup_path_no_ext = backup_path.split(".")[0]
        dated_backups = self._get_dated_backups(backup_path)

        if len(dated_backups) > 0:
            try:
                last_number = int(dated_backups[-1].split("_")[-1].split(".")[0])
                backup_path = f"{backup_path_no_ext}_{str(last_number + 1)}.enc.bak"
            except ValueError:
                backup_path = f"{backup_path_no_ext}_2.enc.bak"

        with open(backup_path, "w") as backup:
            backup.write(store_content)

    def swap_store_with_backup(self, backup_name: str) -> None:
        backup_content = self.get_backup_content(backup_name)
        self.make_backup()

        with open(constants.STORE_FILE, "w+") as store:
            store.write(backup_content)

    def delete_backup(self, backup_name: str) -> None:
        os.remove(os.path.join(constants.STORE_BACKUPS_DIR, backup_name))
