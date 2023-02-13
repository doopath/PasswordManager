from textual import screen
from ..app import App


class Screen(screen.Screen):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.app: App
