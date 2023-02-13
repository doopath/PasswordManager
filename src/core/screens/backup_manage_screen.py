from textual.app import ComposeResult
from textual.containers import Grid, Vertical
from textual.widgets import Button, Header, Label
from .. import constants
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
        yield Header(show_clock=True, id="header")
        yield Vertical(
            *[
                Grid(
                    Grid(
                        Label(backup_name, classes="backup_manage_screen_item_label"),
                        classes="backup_manage_screen_item_label_container",
                    ),
                    Grid(
                        Button(
                            "Restore",
                            classes="button backup_manage_screen_item_button",
                            id=f"backup_restore_button_BACKUP={backup_name}",
                        ),
                        Button(
                            "Delete",
                            classes="button backup_manage_screen_item_button",
                            id=f"backup_delete_button_BACKUP={backup_name}",
                        ),
                        classes="backup_manage_screen_item_buttons_container",
                    ),
                    classes="backup_manage_screen_item",
                )
                for backup_name in self.store_backup.get_backups_names()
            ],
            Grid(
                Button(
                    "Create backup",
                    classes="backup_manage_screen_button button",
                    id="backup_manage_screen_create_button",
                ),
                Button(
                    "To Main Menu",
                    classes="backup_manage_screen_button button",
                    id="backup_manage_screen_to_main_menu_button",
                ),
                Button(
                    "Exit",
                    classes="backup_manage_screen_button button",
                    id="backup_manage_screen_exit_button",
                ),
                classes="backup_manage_screen_buttons_container",
            ),
            classes="backup_manage_screen_container",
        )

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
