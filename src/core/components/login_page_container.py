from typing import Callable
from textual.widgets import Input, Button
from textual.containers import Vertical
from textual.app import ComposeResult


class LoginPageContainer(Vertical):
    def __init__(self, *args, **kwargs):
        self.set_store: Callable[[str], None] = kwargs.pop("set_store")
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Password for the store", id="password_input")
        yield Button(
            label="Login",
            id="login_button",
        )

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "login_button":
            self.set_store(
                self.screen.get_widget_by_id("password_input").__getattribute__("value")
            )
