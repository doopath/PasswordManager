from typing import Callable

from textual.app import ComposeResult
from textual.widgets import Button

from .screen import Screen
from ..components.pair_handle_page import PairHandlePage, PairHandlePageCustomization


class SettingsPairHandleScreen(Screen):
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
        self.value = value
        self.key_input_field_id = "pair_update_key_input"
        self.value_input_field_id = "pair_update_password_input"
        self.update_button_id = "pair_update_button"
        self.back_button_id = "pair_back_button"
        self.button_text = button_text
        super().__init__(*args, **kwargs)

    def _clean_ascii(self, text: str) -> str:
        return text.encode("utf-8").replace(b"\x00", b"").decode("utf-8")

    def _submit(self) -> None:
        key: str = self.get_widget_by_id(self.key_input_field_id).__getattribute__(
            "value"
        )
        value: str = self.get_widget_by_id(
            self.value_input_field_id
        ).__getattribute__("value")

        self.callback(key, value)

    def compose(self) -> ComposeResult:
        yield PairHandlePage(PairHandlePageCustomization(
            key=self.key,
            value=self.value,
            button_text=self.button_text
        )).create()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == self.update_button_id:
            self._submit()
        elif event.button.id == self.back_button_id:
            self.app.pop_screen()
