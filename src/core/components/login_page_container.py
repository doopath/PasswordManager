from typing import Callable
from textual.widgets import Input, Button
from textual.events import Paste
from textual.containers import Vertical
from textual.app import ComposeResult


class LoginPageContainer(Vertical):
    def __init__(self, *args, **kwargs):
        self.set_store: Callable[[str], None] = kwargs.pop("set_store")
        self.button_id = "login_button"
        self.input_id = "login_input"
        self.button_label = (
            kwargs.pop("button_label", "button label")
            if "button_label" in kwargs
            else "Log in"
        )
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        yield Input(
            placeholder="Password for the store",
            id=self.input_id,
            classes="input_form_input_field input_field",
        )
        yield Button(
            label=self.button_label,
            id=self.button_id,
            classes="button input_form_button",
        )

    def on_paste(self, event: Paste) -> None:
        event.stop()
        # Almost all of the terminal emulators are pasting the text by Ctrl+V,
        # so it's needed to avoid double pasting.

    def on_button_pressed(self, event: Button.Pressed):
        event.button.has_focus = False
        if event.button.id == self.button_id:
            self.set_store(
                self.screen.get_widget_by_id(self.input_id).__getattribute__("value")
            )
