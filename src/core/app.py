from textual import app
from .store import Store
from textual.screen import Screen


class App(app.App):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.store: Store | None

    def apply_screen(
        self, screen: Screen, pop: bool = True, name: str | None = None
    ) -> None:
        ...
