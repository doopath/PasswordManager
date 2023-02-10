from textual.app import ComposeResult
from textual.widgets import Static
from textual.containers import Grid
from textual.widget import Widget
from typing import Callable
from .login_page_container import LoginPageContainer


class SignUpPage:
    def __init__(self, set_store: Callable[[str], None]):
        self.set_store = set_store

    def create(self) -> Widget:
        return Grid(
            Static(),
            Grid(
                Static(),
                LoginPageContainer(
                    set_store=self.set_store,
                    button_label="Sign up",
                    classes="input_form_container",
                ),
                Static(),
                classes="input_form_super_container",
            ),
            Static(),
            classes="input_form_grid",
        )
