from typing import Callable
from textual.widgets import Input, Button
from textual.events import Paste
from textual.containers import Vertical, Grid
from textual.app import ComposeResult


class LoginPageContainer(Vertical):
    def __init__(self, *args, **kwargs):
        self.set_store: Callable[[str], None] = kwargs.pop("set_store")
        self.action_button_id = "login_button"
        self.main_menu_button_id = "back_button"
        self.input_id = "login_input"
        self.action_button_label = (
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

    def on_button_pressed(self, event: Button.Pressed):
        event.button.has_focus = False
        if event.button.id == self.action_button_id:
            self.set_store(
                self.screen.get_widget_by_id(self.input_id).__getattribute__("value")
            )
        elif event.button.id == self.main_menu_button_id:
            self.app.pop_screen()
            self.app.push_screen("MainMenuScreen")
