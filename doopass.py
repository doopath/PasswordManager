""" A python module that helps you to manage your secret data. """
import os
import sys
from src.core.app import App
from src.core import constants
from src.core.screens.main_screen import MainScreen
from src.core.screens.screen import Screen


class Doopass(App):
    CSS_PATH = "assets/styles.css"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        constants.update(os.path.dirname(os.path.abspath(__file__)))

    def on_mount(self) -> None:
        main_screen = MainScreen(self)
        self.install_screen(main_screen, name="MainScreen")
        self.push_screen(main_screen)
        self.screen.styles.background = "black"

    def apply_screen(self, screen: Screen, pop: bool = True) -> None:
        screen.styles.background = "black"
        self.app.install_screen(screen)

        if pop:
            self.app.pop_screen()

        self.app.push_screen(screen)


def main() -> int:
    app = Doopass()
    app.run()

    return 0


if __name__ == "__main__":
    sys.exit(main())
