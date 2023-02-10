#! /usr/bin/env python3
""" A python module that helps you to manage your secret data. """

import sys
from src.core.app import App
from src.core.screens.main_screen import MainScreen


class Doopass(App):
    CSS_PATH = "assets/styles.css"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_mount(self) -> None:
        main_screen = MainScreen(self)

        self.install_screen(main_screen)
        self.push_screen(main_screen)
        self.screen.styles.background = "black"


def main() -> int:
    app = Doopass()
    app.run()

    return 0


if __name__ == "__main__":
    sys.exit(main())
