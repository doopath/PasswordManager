from typing import Any, Callable
from ..components.message import Message
from .screen import Screen
from textual.app import ComposeResult
from textual.widgets import Button, Static
from textual.containers import Horizontal


class MessageScreen(Screen):
    def __init__(self, callback: Callable[[], Any], text: str, *args, **kwargs) -> None:
        self.text = text
        self.callback = callback
        super().__init__(*args, **kwargs)
        self.styles.background = "black"

    def compose(self) -> ComposeResult:
        yield Horizontal(
            Static(classes="message_before"),
            Message(text=self.text),
            Static(classes="message_after"),
            classes="message_container",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        event.button.has_focus = False
        self.callback()
