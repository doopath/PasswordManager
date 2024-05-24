from typing import Any

from textual.app import ComposeResult
from textual.containers import Grid
from textual.widgets import Button, Label


class StoreHandleMenuItem(Grid):
    def __init__(self, key: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.key = key

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(self.key, classes="store_handle_item_label"),
            classes="store_handle_item_label_container",
        )
        yield Grid(
            Button(
                "Copy",
                classes="store_handle_item_button button",
                id=f"HANDLE_COPY_KEY={self.key}",
            ),
            Button(
                "Update",
                classes="store_handle_item_button button",
                id=f"HANDLE_UPDATE_KEY={self.key}",
            ),
            Button(
                "Delete",
                classes="store_handle_item_button button",
                id=f"HANDLE_DELETE_KEY={self.key}",
            ),
            classes="store_handle_item_buttons_container",
        )
