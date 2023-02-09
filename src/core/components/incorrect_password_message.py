from typing import Callable
from textual.containers import Vertical
from textual.app import ComposeResult
from textual.widgets import Label, Button


class IncorrectPasswordMessage(Vertical):
    def __init__(self, *args, **kwargs):
        if not "id" in kwargs:
            kwargs["id"] = "incorrect_password_message"

        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        yield Label("Incorrect password!", id="incorrect_password_message_label")
        yield Button(label="OK", id="incorrect_password_message_button")
