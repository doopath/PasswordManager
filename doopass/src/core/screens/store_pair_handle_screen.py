from typing import Callable
from textual.app import ComposeResult
from textual.containers import Grid, Vertical
from textual.widgets import Button, Label, Input
from .screen import Screen
from ..components.store_pair_handle_page import StorePairHandlePage


class StorePairHandleScreen(Screen):
    def __init__(
        self,
        callback: Callable[[str, str], None],
        key: str,
        value: str,
        button_text: str,
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

    def _clean_ascii(self, text: str) -> str:
        return text.encode("utf-8").replace(b"\x00", b"").decode("utf-8")

    def _submit(self) -> None:
        key: str = self.get_widget_by_id(self.key_input_field_id).__getattribute__(
            "value"
        )
        password: str = self.get_widget_by_id(
            self.password_input_field_id
        ).__getattribute__("value")

        self.callback(key, self._clean_ascii(password))

    def compose(self) -> ComposeResult:
        yield StorePairHandlePage(
            self.key, self.password_value, self.button_text
        ).create()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == self.update_button_id:
            self._submit()
        elif event.button.id == self.back_button_id:
            self.app.pop_screen()
