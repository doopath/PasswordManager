from typing import Callable
from textual.app import ComposeResult
from textual.containers import Grid, Vertical
from textual.widgets import Button, Label, Input
from .screen import Screen


class StorePairUpdateScreen(Screen):
    def __init__(
        self,
        callback: Callable[[str, str], None],
        key: str,
        value: str,
        button_text: str = "Update",
        *args,
        **kwargs
    ) -> None:
        self.callback = callback
        self.key = key
        self.password_value = value
        self.key_input_field_id = "store_pair_update_key_input"
        self.password_input_field_id = "store_pair_update_password_input"
        self.update_button_id = "store_pair_update_button"
        self.back_button_id = "store_pair_back_button"
        self.button_text = button_text
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        yield Vertical(
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

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == self.update_button_id:
            key: str = self.get_widget_by_id(self.key_input_field_id).__getattribute__(
                "value"
            )
            password: str = self.get_widget_by_id(
                self.password_input_field_id
            ).__getattribute__("value")
            self.callback(key, password)
        elif event.button.id == self.back_button_id:
            self.callback(self.key, self.password_value)
