from typing import Any, Callable, Dict, List, Tuple

from textual.app import ComposeResult
from textual.containers import Grid
from textual.widgets import Button, Label, Static

from .. import constants


class SelectMenu(Grid):
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
            kwargs["classes"] += " select_menu"
        else:
            kwargs["classes"] = "select_menu"

    def _add_buttons_ids(self) -> None:
        self.numbered_buttons = [
            (b[0], b[1], f"select_menu_button_{self.buttons.index(b)}")
            for b in self.buttons
        ]

    def _add_buttons_map(self) -> None:
        for button in self.numbered_buttons:
            self.buttons_map[button[2]] = button[1]

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(constants.DOOPASS_LOGO, classes="select_menu_logo_label"),
            classes="select_menu_logo_label_container",
        )
        yield Grid(
            Static(),
            Grid(
                *[
                    Button(button[0], classes="select_menu_button button", id=button[2])
                    for button in self.numbered_buttons
                ],
                classes="select_menu_buttons_container",
            ),
            Static(),
            classes="select_menu_buttons_supercontainer",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        event.button.has_focus = False
        try:
            self.buttons_map[str(event.button.id)]()
        except KeyError:
            pass
