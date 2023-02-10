from textual import app
from .store import Store


class App(app.App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.store: Store | None
