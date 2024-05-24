from textual.app import ComposeResult
from textual.widgets import Button, Header

from .. import constants
from ..components.backup_manage_menu import BackupManageMenu
from ..store_backup import StoreBackup
from .screen import Screen


class BackupManageScreen(Screen):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.store_backup = StoreBackup()

    def _update_screen(self) -> None:
        screen = BackupManageScreen()
        self.app.apply_screen(screen)

    def _handle_restore_button(self, backup_name: str) -> None:
        self.store_backup.swap_store_with_backup(
            backup_name + constants.STORE_BACKUP_EXTENSION
        )
        self._update_screen()

    def _handle_delete_button(self, backup_name: str) -> None:
        self.store_backup.delete_backup(backup_name + constants.STORE_BACKUP_EXTENSION)
        self._update_screen()

    def _handle_exit_button(self) -> None:
        self.app.exit()

    def _handle_to_main_menu_button(self) -> None:
        self.app.pop_screen()
        self.app.push_screen("MainMenuScreen")

    def _handle_create_button(self) -> None:
        self.store_backup.make_backup()
        self._update_screen()

    def compose(self) -> ComposeResult:
        backups_names = self.store_backup.get_backups_names()

        yield Header(show_clock=True, id="header")
        yield BackupManageMenu(backups_names)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        event.button.has_focus = False
        id = str(event.button.id)

        if id == "backup_manage_screen_exit_button":
            self._handle_exit_button()
        elif id == "backup_manage_screen_to_main_menu_button":
            self._handle_to_main_menu_button()
        elif id == "backup_manage_screen_create_button":
            self._handle_create_button()
        elif str(id).startswith("backup_restore_button_BACKUP="):
            self._handle_restore_button(id.split("=")[1])
        elif str(id).startswith("backup_delete_button_BACKUP="):
            self._handle_delete_button(id.split("=")[1])
