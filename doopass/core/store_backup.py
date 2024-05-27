import datetime
import logging
import os
from collections import namedtuple
from typing import List

from .settings import config as cfg

# Proxy configuration
Settings = namedtuple('Settings', ['store_file', 'backups', 'backup_extension'])
Config = namedtuple('Config', ['appdata_dir', 'settings'])
config = Config(appdata_dir=cfg.appdata_dir, settings=Settings(
    store_file=cfg.settings['local']['store_file'],
    backups=cfg.settings['local']['backups'],
    backup_extension=cfg.settings['local']['backup_extension']
))


class StoreBackup:
    def __init__(self) -> None:
        self._initialize_backup_dir()

    def _initialize_backup_dir(self) -> None:
        if not os.path.isdir(config.appdata_dir):
            logging.debug("The appdata directory doesn't exist; creating it")
            os.mkdir(config.appdata_dir)
            logging.debug("The appdata directory has been created")

        if not os.path.isdir(config.settings.backups):
            logging.debug("The store backups directory doesn't exist; creating it")
            os.mkdir(config.settings.backups)
            logging.debug("The store backups directory has been created")

    def _get_file_content(self, filepath: str) -> str:
        content = ""

        with open(filepath, "r") as store:
            content = store.read()

        return content

    def _get_dated_backups(self, base: str) -> List[str]:
        backups = os.listdir(config.settings.backups)
        dated_backups = [
            b for b in backups if b.startswith(base) and b.endswith(".enc.bak")
        ]

        return sorted(dated_backups)

    def get_store_content(self) -> str:
        return self._get_file_content(config.settings.store_file)

    def get_backups_names(self) -> List[str]:
        backups = os.listdir(config.settings.backups)
        backups = [b for b in backups if b.endswith(".enc.bak")]
        return [".".join(b.split(".")[:-2]) for b in backups]

    def get_backup_content(self, backup_name: str) -> str:
        backup_path = os.path.join(config.settings.backups, backup_name)
        return self._get_file_content(backup_path)

    def make_backup(self) -> None:
        logging.debug("Making a backup of the store")
        date = datetime.date.today()
        current_date = date.strftime("%d_%m_%Y")
        store_name = config.settings.store_file.split(os.path.sep)[-1]
        backup_name = f"{str(current_date)}_{store_name.removesuffix('.enc')}_1{config.settings.backup_extension}"
        store_content = self.get_store_content()
        backup_path = os.path.join(config.settings.backups, backup_name)
        backup_path_no_ext = "_".join(backup_path.split(".")[0].split("_")[:-1])
        store_base_name = store_name.removesuffix(".enc")
        dated_backups = self._get_dated_backups(
            f"{str(current_date)}_{store_base_name}"
        )

        if len(dated_backups) > 0:
            try:
                last_number = int(dated_backups[-1].split("_")[-1].split(".")[0])
                backup_path = f"{backup_path_no_ext}_{str(last_number + 1)}{config.settings.backup_extension}"
            except ValueError:
                backup_path = (
                    f"{backup_path_no_ext}_2{config.settings.backup_extension}"
                )

        with open(backup_path, "w") as backup:
            backup.write(store_content)

        logging.debug("A backup of the store has been created")

    def swap_store_with_backup(self, backup_name: str) -> None:
        logging.debug(f"Swapping the store with a backup BACKUP_NAME={backup_name}")
        backup_content = self.get_backup_content(backup_name)
        self.make_backup()

        with open(config.settings.store_file, "w+") as store:
            store.write(backup_content)

        logging.debug(
            f"The store has been swapped with the backup BACKUP_NAME={backup_name}"
        )

    def delete_backup(self, backup_name: str) -> None:
        logging.debug(f"Deleting a backup BACKUP_NAME={backup_name}")
        os.remove(os.path.join(config.settings.backups, backup_name))
        logging.debug(f"The backup has been deleted BACKUP_NAME={backup_name}")
