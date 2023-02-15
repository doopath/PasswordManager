import logging
from typing import Callable
from textual.app import ComposeResult
from .screen import Screen
from .message_screen import MessageScreen
from .. import store
from textual.widgets import Header, Button

from ..components.signup_page import SignUpPage


class SignUpScreen(Screen):
    def __init__(self, set_store: Callable[[str], None], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.styles.background = "black"
        self.set_store_callback = set_store

    def _show_main_screen(self) -> None:
        self.app.push_screen("MainMenuScreen")

    def _show_store_exists_message(self) -> None:
        def callback() -> None:
            self.app.pop_screen()
            self._show_main_screen()

        screen = MessageScreen(callback=callback, text="Store already exists!")
        screen.styles.background = "black"
        self.app.install_screen(screen)
        self.app.pop_screen()
        self.app.push_screen(screen)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, id="header")
        yield SignUpPage(set_store=self.set_store).create()

    def set_store(self, password: str) -> None:
        logging.debug("Setting store")

        if store.does_store_file_exist():
            logging.debug("Trying to create a store, that already exists")
            self._show_store_exists_message()
            return

        store.try_initialize_store(password)
        logging.debug("Creating a new store")
        self.set_store_callback(password)
