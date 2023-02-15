from typing import Callable

from textual import events
from textual.app import ComposeResult
from textual.containers import Grid, Vertical
from textual.events import Paste
from textual.widgets import Button, Input


class LoginPageContainer(Vertical):
    def __init__(self, *args, **kwargs):
        self.set_store_callback: Callable[[str], None] = kwargs.pop("set_store")
        self.action_button_id = "login_button"
        self.main_menu_button_id = "back_button"
        self.input_id = "login_input"
        self.action_button_label = (
            kwargs.pop("button_label", "button label")
            if "button_label" in kwargs
            else "Log in"
        )
        super().__init__(*args, **kwargs)

    def _create_input_field(self) -> Input:
        input_field = Input(
            placeholder="Password for the store",
            id=self.input_id,
            classes="input_form_input_field input_field",
            password=True,
        )
        input_field.focus()
        return input_field

    def _set_store(self) -> None:
        self.set_store_callback(
            self.screen.get_widget_by_id(self.input_id).__getattribute__("value")
        )

    def compose(self) -> ComposeResult:
        yield self._create_input_field()
        yield Grid(
            Button(
                label=self.action_button_label,
                id=self.action_button_id,
                classes="button input_form_button",
            ),
            Button(
                label="To Main Menu",
                id=self.main_menu_button_id,
                classes="button input_form_button",
            ),
            classes="input_form_buttons_container",
        )

    def on_paste(self, event: Paste) -> None:
        event.stop()
        # Almost all of the terminal emulators are pasting the text by Ctrl+V,
        # so it's needed to avoid double pasting.

    def on_key(self, event: events.Key):
        if event.key == "enter" and self.get_widget_by_id(self.input_id).has_focus:
            event.stop()
            self._set_store()

    def on_button_pressed(self, event: Button.Pressed):
        event.button.has_focus = False
        if event.button.id == self.action_button_id:
            self._set_store()
        elif event.button.id == self.main_menu_button_id:
            self.app.pop_screen()
            self.app.push_screen("MainMenuScreen")
