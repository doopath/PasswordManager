from textual.app import ComposeResult
from textual.widgets import Static, Header
from .screen import Screen
from ..store import Store


class StoreHandleScreen(Screen):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def on_mount(self) -> None:
        self.styles.background = "black"

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, id="header")
        yield Static()
        self.app.store
