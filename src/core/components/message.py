from typing import Callable
from textual.containers import Vertical
from textual.app import ComposeResult
from textual.widgets import Label, Button


class Message(Vertical):
    def __init__(self, *args, **kwargs):
        self.text = kwargs.pop("text")

        if not "id" in kwargs:
            kwargs["id"] = "message"

        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        yield Label(self.text, id="message_label")
        yield Button(label="OK", id="message_button", classes="button")
