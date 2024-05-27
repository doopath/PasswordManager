import base64

from textual.app import ComposeResult
from textual.containers import Grid
from textual.widgets import Button, Label


class StoreHandleMenuItem(Grid):
    def __init__(self, key: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.key = base64.b16encode(key.encode())

    def compose(self) -> ComposeResult:
        readable_key = base64.b16decode(self.key).decode()
        base_key = self.key.decode()
        yield Grid(
            Label(readable_key, classes="store_handle_item_label"),
            classes="store_handle_item_label_container",
        )
        yield Grid(
            Button(
                "Copy",
                classes="store_handle_item_button button",
                id=f"HANDLE_COPY_STORE-{base_key}",
            ),
            Button(
                "Update",
                classes="store_handle_item_button button",
                id=f"HANDLE_UPDATE_STORE-{base_key}",
            ),
            Button(
                "Delete",
                classes="store_handle_item_button button",
                id=f"HANDLE_DELETE_STORE-{base_key}",
            ),
            classes="store_handle_item_buttons_container",
        )
