from typing import Any, Callable

from textual.app import ComposeResult
from textual.widgets import Header

from ..components.select_menu import SelectMenu
from .login_screen import LoginScreen
from .backup_manage_screen import BackupManageScreen
from .screen import Screen
from .sign_up_screen import SignUpScreen


class MainMenuScreen(Screen):
    def __init__(self, set_store: Callable[[str], None], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.set_store = set_store

    def on_mount(self) -> None:
        self.screen.styles.background = "black"

    def _show_screen_wrapper(self, f: Callable[[], None]) -> Callable[[], None]:
        def wrapper() -> None:
            self.app.pop_screen()
            f()

        return wrapper

    def _show_login_screen(self) -> None:
        screen = LoginScreen(set_store=self.set_store)
        self.app.apply_screen(screen)

    def _show_backup_screen(self) -> None:
        screen = BackupManageScreen()
        self.app.apply_screen(screen)

    def _show_sign_up_screen(self) -> None:
        screen = SignUpScreen(set_store=self.set_store)
        self.app.install_screen(screen)
        self.app.push_screen(screen)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, id="header")
        yield SelectMenu(
            [
                ("Log in", self._show_screen_wrapper(self._show_login_screen)),
                ("Backups", self._show_screen_wrapper(self._show_backup_screen)),
                ("Sign up", self._show_screen_wrapper(self._show_sign_up_screen)),
                ("Exit", self.app.exit),
            ]
        )
