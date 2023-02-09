from ..components.incorrect_password_message import IncorrectPasswordMessage
from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Button, Static
from textual.containers import Horizontal


class IncorrectPasswordScreen(Screen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.styles.background = "black"

    def compose(self) -> ComposeResult:
        yield Horizontal(
            Static(id="incorrect_password_message_before"),
            IncorrectPasswordMessage(),
            Static(id="incorrect_password_message_after"),
            id="incorrect_password_message_container",
        )

    def quit_error_screen(self) -> None:
        self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "incorrect_password_message_button":
            self.quit_error_screen()
