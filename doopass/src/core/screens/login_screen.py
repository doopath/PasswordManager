from typing import Callable

from textual.app import ComposeResult
from textual.widgets import Header

from ..app import App
from ..components.login_page import LoginPage
from .screen import Screen


class LoginScreen(Screen):
    def __init__(self, set_store: Callable[[str], None], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.set_store = set_store

    def on_mount(self) -> None:
        self.screen.styles.background = "black"

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, id="header")
        yield LoginPage(self.set_store).create()
