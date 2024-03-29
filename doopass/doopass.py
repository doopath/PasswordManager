""" A python module that helps you to manage your secret data. """
import logging
import sys

from typing import override

from doopass.src.core.app import App
from doopass.src.core.screens.main_screen import MainScreen
from doopass.src.core.screens.screen import Screen


class Doopass(App):
    def on_mount(self) -> None:
        main_screen = MainScreen(self)
        self.install_screen(main_screen, name="MainScreen")
        self.push_screen(main_screen)
        self.screen.styles.background = "black"
        logging.debug("The app has been launched")

    @override
    def apply_screen(
        self, screen: Screen, pop: bool = True, name: str | None = None
    ) -> None:
        screen.styles.background = "black"

        if name:
            self.app.install_screen(screen, name=name)
        else:
            self.app.install_screen(screen)

        if pop:
            self.app.pop_screen()

        self.app.push_screen(screen)

    def exit(self, result=None, message=None) -> None:
        logging.debug("App exited\n")
        super().exit(result, message)


def main() -> int:
    app = Doopass()
    app.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
