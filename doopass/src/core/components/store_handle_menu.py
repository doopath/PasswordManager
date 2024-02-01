from typing import Any, Callable, List

from textual.app import ComposeResult
from textual.containers import Grid, Vertical
from textual.widgets import Button, Input, Label

from ..components.store_handle_menu_item import StoreHandleMenuItem


class StoreHandleMenu(Vertical):
    def __init__(self, get_keys: Callable[[], List[str]], *args, **kwargs) -> None:
        self._add_classes(kwargs)
        super().__init__(*args, **kwargs)
        self.get_keys = get_keys
        self.search_input_field_id: str
        self.clean_search_button_id: str
        self.exit_button_id: str
        self.to_main_menu_button_id: str
        self.add_pair_button_id: str
        self.store_item_class: str

    def _add_classes(self, kwargs: Any) -> None:
        if not "classes" in kwargs:
            kwargs["classes"] = ""

        kwargs["classes"] += " store_handle_container"

    def compose(self) -> ComposeResult:
        keys = sorted(self.get_keys())
        search_input_field = Input(
            placeholder="Search",
            classes="store_handle_search_input_field input_field",
            id="store_handle_search_input_field",
        )
        search_input_field.focus()

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

        yield Grid(
            search_input_field,
            Button(
                "Clean search",
                classes="store_handle_search_clean_button button",
                id="store_handle_search_clean_button",
            ),
            classes="store_handle_search_container",
        )

        if keys:
            yield Label("Your keys", classes="store_handle_title")
        else:
            yield Label("No store items", classes="store_handle_title")

        for key in sorted(self.get_keys()):
            yield StoreHandleMenuItem(key, classes=self.store_item_class)
