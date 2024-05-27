import base64
from typing import Callable

from textual.app import ComposeResult
from textual.widgets import Button, Header

from .screen import Screen
from .settings_pair_handle_screen import SettingsPairHandleScreen
from ..settings import config
from ..components.settings_handle_page import SettingsHandlePage


class SettingsScreen(Screen):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def _update_screen(self) -> None:
        screen = SettingsScreen()
        self.app.apply_screen(screen)

    def _handle_restore_button(self) -> None:
        config.restore_defaults(callback=self._update_screen)

    def _handle_exit_button(self) -> None:
        self.app.exit()

    def _handle_to_main_menu_button(self) -> None:
        self.app.pop_screen()
        self.app.push_screen("MainMenuScreen")

    def _handle_change_setting_button(self, key: str, section: str) -> None:
        value = config.settings[section][key]
        screen = SettingsPairHandleScreen(
            callback=(lambda k, v: config.modify_property(section, k, v) or self._update_screen()),
            key=key,
            value=value,
            button_text="Update"
        )
        screen.styles.background = "black"
        self.app.apply_screen(screen, pop=False)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, id="header")
        yield SettingsHandlePage()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        event.button.has_focus = False
        id = str(event.button.id)

        if id == "settings_manage_screen_exit_button":
            self._handle_exit_button()
        elif id == "settings_manage_screen_to_main_menu_button":
            self._handle_to_main_menu_button()
        elif id == "settings_restore_button":
            self._handle_restore_button()
        elif str(id).startswith("CHANGE_SETTING_BUTTON-KEY_"):
            # id = f"CHANGE_SETTING_BUTTON-KEY_{key}_{section}"
            key_section = str(id).split('-')[1].split('_')[1:]
            key = base64.b16decode(key_section[0]).decode()
            section = base64.b16decode(key_section[1]).decode()
            self._handle_change_setting_button(key, section)
