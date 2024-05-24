from typing import Callable
from textual.app import ComposeResult
from textual.containers import Grid, Vertical
from textual.widgets import Button, Label, Input
from textual.widget import Widget


class StorePairHandlePage:
    def __init__(self, key: str, value: str, button_text: str) -> None:
        self.key = key
        self.password_value = value
        self.key_input_field_id = "store_pair_update_key_input"
        self.password_input_field_id = "store_pair_update_password_input"
        self.update_button_id = "store_pair_update_button"
        self.back_button_id = "store_pair_back_button"
        self.button_text = button_text

    def create(self) -> Widget:
        return Vertical(
            Grid(
                Grid(
                    Label("Key:", classes="store_pair_update_label"),
                    classes="store_pair_update_label_container",
                ),
                Input(
                    value=self.key,
                    classes="store_pair_update_key_input store_pair_update_input input_field",
                    id=self.key_input_field_id,
                ),
                classes="store_pair_update_attribute_container",
            ),
            Grid(
                Grid(
                    Label("Password:", classes="store_pair_update_label"),
                    classes="store_pair_update_label_container",
                ),
                Input(
                    value=self.password_value,
                    classes="store_pair_update_password_input store_pair_update_input input_field",
                    id=self.password_input_field_id,
                ),
                classes="store_pair_update_attribute_container",
            ),
            Grid(
                Button(
                    self.button_text,
                    classes="store_pair_update_button button",
                    id=self.update_button_id,
                ),
                Button(
                    "Back",
                    classes="store_pair_update_button button",
                    id=self.back_button_id,
                ),
                classes="store_pair_update_buttons_container",
            ),
            classes="store_pair_update_container",
        )
