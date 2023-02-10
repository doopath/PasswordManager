from typing import Any, Callable, Dict, List, Tuple

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button


class MainMenu(Vertical):
    def __init__(self, buttons: List[Tuple[str, Callable[[], None]]], *args, **kwargs):
        self._add_classes(kwargs)
        self.buttons = buttons
        self.numbered_buttons: List[Tuple[str, Callable[[], None], str]] = []
        self.buttons_map: Dict[str, Callable[[], None]] = {}
        self._add_buttons_ids()
        self._add_buttons_map()
        super().__init__(*args, **kwargs)

    def _add_classes(self, kwargs: Any) -> Any:
        if "classes" in kwargs:
            kwargs["classes"] += " main_menu"
        else:
            kwargs["classes"] = "main_menu"

    def _add_buttons_ids(self) -> None:
        self.numbered_buttons = [
            (b[0], b[1], f"menu_button_{self.buttons.index(b)}") for b in self.buttons
        ]

    def _add_buttons_map(self) -> None:
        for button in self.numbered_buttons:
            self.buttons_map[button[2]] = button[1]

    def compose(self) -> ComposeResult:
        for button in self.numbered_buttons:
            yield Button(button[0], classes="main_menu_button button", id=button[2])

    def on_button_pressed(self, event: Button.Pressed) -> None:
        try:
            self.buttons_map[str(event.button.id)]()
        except KeyError:
            pass
