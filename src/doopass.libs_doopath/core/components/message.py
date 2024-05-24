from typing import Callable
from textual.containers import Vertical
from textual.app import ComposeResult
from textual.widgets import Label, Button


class Message(Vertical):
    def __init__(self, *args, **kwargs):
        self.text = kwargs.pop("text")

        if not "classes" in kwargs:
            kwargs["classes"] = "message"
        else:
            kwargs["classes"] += " message"

        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        button = Button(
            label="OK", id="message_button", classes="button message_button"
        )
        button.focus()
        yield Label(self.text, id="message_label", classes="message_label")
        yield button
