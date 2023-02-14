from typing import Callable

import pyperclip
from textual.app import ComposeResult
from textual.widgets import Button, Header

from .main_menu_screen import MainMenuScreen
from .screen import Screen
from .store_pair_handle_screen import StorePairHandleScreen
from ..components.store_handle_menu import StoreHandleMenu


class StoreHandleScreen(Screen):
    def __init__(self, set_store: Callable[[str], None], *args, **kwargs) -> None:
        self.set_store = set_store
        super().__init__(*args, **kwargs)

    def _handle_copy_key(self, key: str) -> None:
        assert self.app.store, "Store is not initialized!"
        pyperclip.copy(self.app.store.get_value(key))

    def _handle_delete_key(self, key: str) -> None:
        assert self.app.store, "Store is not initialized!"

        screen = StoreHandleScreen(self.set_store)
        screen.styles.background = "black"
        pyperclip.copy(f"{key}={self.app.store.get_value(key)}")
        self.app.store.remove_property(key)
        self.app.apply_screen(screen)

    def _handle_update_key(self, key: str) -> None:
        assert self.app.store, "Store is not initialized!"
        old_key = key

        def callback(key: str, value: str) -> None:
            assert self.app.store, "Store is not initialized!"

            screen = StoreHandleScreen(self.set_store)
            screen.styles.background = "black"
            self.app.store.remove_property(old_key)
            self.app.store.add_property(key, value)
            self.app.apply_screen(screen)

        password_value = self.app.store.get_value(key)
        screen = StorePairHandleScreen(
            callback=callback, key=key, value=password_value, button_text="Update"
        )
        screen.styles.background = "black"
        self.app.apply_screen(screen)

    def _handle_add_pair(self) -> None:
        def callback(key: str, value: str) -> None:
            assert self.app.store, "Store is not initialized!"

            screen = StoreHandleScreen(self.set_store)
            self.app.store.add_property(key, value)
            self.app.apply_screen(screen)

        screen = StorePairHandleScreen(
            callback=callback, key="", value="", button_text="Add pair"
        )
        screen.styles.background = "black"
        self.app.apply_screen(screen, pop=False)

    def _show_main_menu(self) -> None:
        self.app.pop_screen()
        self.app.push_screen("MainMenuScreen")

    def compose(self) -> ComposeResult:
        assert self.app.store, "Store is not initialized!"

        yield Header(show_clock=True, id="header")
        yield StoreHandleMenu(self.app.store.get_keys)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        id = str(event.button.id)
        event.button.has_focus = False

        if id == "add_pair_button":
            self._handle_add_pair()
        elif id == "to_main_menu_button":
            self._show_main_menu()
        elif id == "exit_button":
            self.app.exit()
        elif id.startswith("HANDLE"):
            button_id = id.split("=")[1]
            if id.startswith("HANDLE_COPY"):
                self._handle_copy_key(button_id)
            elif id.startswith("HANDLE_UPDATE"):
                self._handle_update_key(button_id)
            elif id.startswith("HANDLE_DELETE"):
                self._handle_delete_key(button_id)
