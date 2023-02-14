from typing import Any, Callable, List

from textual.app import ComposeResult
from textual.containers import Grid, Vertical
from textual.widgets import Button, Label


class StoreHandleMenu(Vertical):
    def __init__(self, get_keys: Callable[[], List[str]], *args, **kwargs) -> None:
        self._add_classes(kwargs)
        super().__init__(*args, **kwargs)
        self.get_keys = get_keys

    def _add_classes(self, kwargs: Any) -> None:
        if not "classes" in kwargs:
            kwargs["classes"] = ""

        kwargs["classes"] += " store_handle_container"

    def compose(self) -> ComposeResult:
        keys = sorted(self.get_keys())

        yield Grid(
            Button(
                "Add pair",
                classes="store_handle_button button",
                id="add_pair_button",
            ),
            Button(
                "To Main Menu",
                classes="store_handle_button button",
                id="to_main_menu_button",
            ),
            Button(
                "Exit",
                classes="store_handle_button button",
                id="exit_button",
            ),
            classes="store_handle_buttons_container",
        )

        if keys:
            yield Label("Your keys", classes="store_handle_title")
        else:
            yield Label("No store items", classes="store_handle_title")

        for key in sorted(self.get_keys()):
            yield Grid(
                Grid(
                    Label(key, classes="store_handle_item_label"),
                    classes="store_handle_item_label_container",
                ),
                Grid(
                    Button(
                        "Copy",
                        classes="store_handle_item_button button",
                        id=f"HANDLE_COPY_KEY={key}",
                    ),
                    Button(
                        "Update",
                        classes="store_handle_item_button button",
                        id=f"HANDLE_UPDATE_KEY={key}",
                    ),
                    Button(
                        "Delete",
                        classes="store_handle_item_button button",
                        id=f"HANDLE_DELETE_KEY={key}",
                    ),
                    classes="store_handle_item_buttons_container",
                ),
                classes="store_handle_item",
            )
