from .screen import Screen
from textual.app import ComposeResult
from textual.widgets import Header
from textual.containers import Grid, Vertical


class BackupManageScreen(Screen):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, id="header")
        yield Vertical(classes="backup_manage_screen_container")
