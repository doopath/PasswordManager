from typing import Callable
from ..app import App
from .login_screen import LoginScreen
from .screen import Screen
from ..components.main_menu import MainMenu
from textual.widgets import Header
from textual.app import ComposeResult


class MainMenuScreen(Screen):
    def __init__(
        self, set_store: Callable[[str], None], app: App, *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.set_store = set_store

    def on_mount(self) -> None:
        self.screen.styles.background = "black"

    def _show_login_screen(self) -> None:
        screen = LoginScreen(set_store=self.set_store, app=self.app)
        self.app.install_screen(screen)
        self.app.push_screen(screen)

    def _show_backup_screen(self) -> None:
        pass

    def _show_sign_up_screen(self) -> None:
        pass

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, id="header")
        yield MainMenu(
            [
                ("Login", self._show_login_screen),
                ("Backup", self._show_backup_screen),
                ("Sign up", self._show_sign_up_screen),
                ("Exit", self.app.exit),
            ]
        )
