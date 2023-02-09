from typing import Callable
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Button

from ..components.signup_page import SignUpPage


class SignUpScreen(Screen):
    def __init__(self, callback: Callable[[str], None], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.styles.background = "black"
        self.callback = callback

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, id="header")
        yield SignUpPage(set_store=self.callback).create()
