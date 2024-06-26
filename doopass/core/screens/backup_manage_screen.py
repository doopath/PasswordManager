import base64

from textual.app import ComposeResult
from textual.widgets import Button, Header

from .screen import Screen
from ..components.backup_manage_menu import BackupManageMenu
from ..settings import config
from ..store_backup import StoreBackup


class BackupManageScreen(Screen):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.store_backup = StoreBackup()

    def _update_screen(self) -> None:
        screen = BackupManageScreen()
        self.app.apply_screen(screen)

    def _handle_restore_button(self, backup_name: str) -> None:
        self.store_backup.swap_store_with_backup(
            backup_name + config.settings.backup_extension
        )
        self._update_screen()

    def _handle_delete_button(self, backup_name: str) -> None:
        self.store_backup.delete_backup(backup_name + config.settings.backup_extension)
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

        if str(id).startswith("HANDLE"):
            key = base64.b16decode(id.split("-")[1].encode()).decode()

            if str(id).startswith("HANDLE_RESTORE_BACKUP"):
                self._handle_restore_button(key)
            if str(id).startswith("HANDLE_DELETE_BACKUP"):
                self._handle_delete_button(key)
