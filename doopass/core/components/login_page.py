from typing import Callable

from textual.containers import Grid
from textual.widget import Widget
from textual.widgets import Static

from .login_page_container import LoginPageContainer


class LoginPage:
    def __init__(self, set_store: Callable[[str], None]):
        self.set_store = set_store

    def create(self) -> Widget:
        return Grid(
            Static(),
            Grid(
                Static(),
                LoginPageContainer(
                    set_store=self.set_store,
                    id="login_container",
                    classes="input_form_container",
                ),
                Static(),
                id="login_super_container",
                classes="input_form_super_container",
            ),
            Static(),
            id="login_grid",
            classes="input_form_grid",
        )
