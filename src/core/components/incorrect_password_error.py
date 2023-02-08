from typing import Callable
from textual.containers import Horizontal
from textual.app import ComposeResult
from textual.widgets import Label, Button


class IncorrectPasswordError(Horizontal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        yield Label("Incorrect password!", id="incorrect_password_error_label")
        yield Button(label="OK", id="incorrect_password_error_button")
