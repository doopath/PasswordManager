from typing import List
from textual.app import ComposeResult
from textual.containers import Grid, Vertical
from textual.widgets import Button, Label


class BackupManageMenu(Vertical):
    def __init__(self, backups_names: List[str], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.backups_names = backups_names

    def compose(self) -> ComposeResult:
        yield Vertical(
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
            Label("Your backups", classes="backup_manage_screen_no_backups_label")
            if self.backups_names
            else Label("No backups", classes="backup_manage_screen_no_backups_label"),
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
                for backup_name in self.backups_names
            ],
            classes="backup_manage_screen_container",
        )
