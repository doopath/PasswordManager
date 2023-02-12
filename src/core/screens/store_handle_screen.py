from typing import Callable
import pyperclip
from textual.app import ComposeResult
from textual.widgets import Label, Header, Button
from textual.containers import Vertical, Horizontal, Grid
from .screen import Screen
from .main_menu_screen import MainMenuScreen
from .store_pair_update_screen import StorePairUpdateScreen


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
        screen = StorePairUpdateScreen(
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

        screen = StorePairUpdateScreen(
            callback=callback, key="", value="", button_text="Add pair"
        )
        screen.styles.background = "black"
        self.app.apply_screen(screen)

    def _show_main_menu(self) -> None:
        screen = MainMenuScreen(self.set_store)
        screen.styles.background = "black"
        self.app.apply_screen(screen)

    def compose(self) -> ComposeResult:
        assert self.app.store, "Store is not initialized!"

        yield Header(show_clock=True, id="header")
        yield Vertical(
            Label("Your keys", classes="store_handle_title"),
            *[
                Grid(
                    Grid(
                        Label(key, classes="store_handle_item_label"),
                        classes="store_handle_item_label_container",
                    ),
                    Grid(
                        Button(
                            "Copy",
                            classes="store_handle_item_button button",
                            id=f"HANDLE_COPY_KEY={key}",
                        ),
                        Button(
                            "Update",
                            classes="store_handle_item_button button",
                            id=f"HANDLE_UPDATE_KEY={key}",
                        ),
                        Button(
                            "Delete",
                            classes="store_handle_item_button button",
                            id=f"HANDLE_DELETE_KEY={key}",
                        ),
                        classes="store_handle_item_buttons_container",
                    ),
                    classes="store_handle_item",
                )
                for key in self.app.store.get_keys()
            ],
            Grid(
                Button(
                    "Add pair",
                    classes="store_handle_button button",
                    id="add_pair_button",
                ),
                Button(
                    "To Main Menu",
                    classes="store_handle_button button",
                    id="to_main_menu_button",
                ),
                Button(
                    "Exit",
                    classes="store_handle_button button",
                    id="exit_button",
                ),
                classes="store_handle_buttons_container",
            ),
            classes="store_handle_container",
        )

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
