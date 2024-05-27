from textual.app import ComposeResult
from textual.containers import Grid, VerticalScroll
from textual.widgets import Button
from .settings_pairs_list import SettingsPairsList
from ..settings import config


class SettingsHandlePage(VerticalScroll):
    def __init__(self, *args, **kwargs):
        kwargs['classes'] = "settings_handle_page_container"
        super().__init__(*args, **kwargs)
        self.exit_button_id = "settings_manage_screen_exit_button"
        self.main_menu_button_id = "settings_manage_screen_to_main_menu_button"
        self.restore_defaults_button_id = "settings_restore_button"
        self.keys = config.settings.keys()

    def compose(self) -> ComposeResult:
        yield Grid(
            Button(
                "Restore",
                classes="settings_manage_screen_button button",
                id=self.restore_defaults_button_id
            ),
            Button(
                "Main Menu",
                classes="settings_manage_screen_button button",
                id=self.main_menu_button_id
            ),
            Button(
                "Exit",
                classes="settings_manage_screen_button button",
                id=self.exit_button_id
            ),
            classes="settings_handle_page_buttons_container"
        )

        for key in self.keys:
            yield SettingsPairsList(key, key[0].upper() + key[1:])
