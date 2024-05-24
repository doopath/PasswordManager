import asyncio
from typing import Callable

import pyperclip
from textual import events
from textual.app import ComposeResult
from textual.widgets import Button, Header

from ..components.store_handle_menu import StoreHandleMenu
from ..components.store_handle_menu_item import StoreHandleMenuItem
from .screen import Screen
from .store_pair_handle_screen import StorePairHandleScreen


class StoreHandleScreen(Screen):
    def __init__(self, set_store: Callable[[str], None], *args, **kwargs) -> None:
        self.set_store = set_store
        super().__init__(*args, **kwargs)
        self.search_input_field_id = "store_handle_search_input_field"
        self.clean_search_button_id = "store_handle_search_clean_button"
        self.exit_button_id = "exit_button"
        self.to_main_menu_button_id = "to_main_menu_button"
        self.add_pair_button_id = "add_pair_button"
        self.store_item_class = "store_handle_item"

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
        self.app.apply_screen(screen, pop=False)

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

    async def _remove_items(self) -> None:
        items = list(self.children[1].children)

        for item in items:
            if self.store_item_class in item.classes:
                await item.remove()

    async def _filter_items_by_str(self, finding_key: str) -> None:
        assert self.app.store, "Store is not initialized!"

        items_container = self.children[1]
        await self._remove_items()

        for key in sorted(self.app.store.get_keys()):
            if key.lower().find(finding_key.lower()) != -1:
                await items_container.mount(
                    StoreHandleMenuItem(key, classes=self.store_item_class)
                )

    def _run_filter_items_by_str(self, finding_key: str) -> None:
        loop = asyncio.get_running_loop()
        loop.create_task(self._filter_items_by_str(finding_key))

    def _filter_items_by_input(self) -> None:
        key = str(
            self.get_widget_by_id(self.search_input_field_id).__getattribute__("value")
        )
        self._run_filter_items_by_str(key)

    def _clean_search(self) -> None:
        self._run_filter_items_by_str("")
        self.get_widget_by_id(self.search_input_field_id).__setattr__("value", "")

    def _setup_menu(self) -> StoreHandleMenu:
        assert self.app.store, "Store is not initialized!"

        menu = StoreHandleMenu(self.app.store.get_keys)
        menu.search_input_field_id = self.search_input_field_id
        menu.clean_search_button_id = self.clean_search_button_id
        menu.exit_button_id = self.exit_button_id
        menu.to_main_menu_button_id = self.to_main_menu_button_id
        menu.add_pair_button_id = self.add_pair_button_id
        menu.store_item_class = self.store_item_class

        return menu

    def on_key(self, event: events.Key) -> None:
        if (
            event.key == "enter"
            and self.get_widget_by_id(self.search_input_field_id).has_focus
        ):
            event.stop()
            self._filter_items_by_input()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, id="header")
        yield self._setup_menu()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        id = str(event.button.id)
        event.button.has_focus = False

        if id == self.add_pair_button_id:
            self._handle_add_pair()
        elif id == self.to_main_menu_button_id:
            self._show_main_menu()
        elif id == self.exit_button_id:
            self.app.exit()
        elif id == self.clean_search_button_id:
            self._clean_search()
        elif id.startswith("HANDLE"):
            button_id = id.split("=")[1]
            if id.startswith("HANDLE_COPY"):
                self._handle_copy_key(button_id)
            elif id.startswith("HANDLE_UPDATE"):
                self._handle_update_key(button_id)
            elif id.startswith("HANDLE_DELETE"):
                self._handle_delete_key(button_id)
