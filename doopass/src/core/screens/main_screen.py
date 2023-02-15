import logging
from typing import Any, Callable

from .. import store
from ..exceptions import StoreIsNotInitializedError
from ..password_validation import PasswordValidator
from .main_menu_screen import MainMenuScreen
from .message_screen import MessageScreen
from .screen import Screen
from .sign_up_screen import SignUpScreen
from .store_handle_screen import StoreHandleScreen


class MainScreen(Screen):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def on_mount(self) -> None:
        screen = MainMenuScreen(set_store=self.set_store)
        screen.styles.background = "black"
        self.app.install_screen(screen, name="MainMenuScreen")
        self.app.push_screen(screen)

    def _show_message(self, callback: Callable[[], Any], text: str) -> None:
        message_screen = MessageScreen(callback, text)
        message_screen.styles.background = "black"
        self.app.install_screen(message_screen)
        self.app.push_screen(message_screen)

    def _show_incorrect_password_message(self) -> None:
        self._show_message(self.app.pop_screen, "Incorrect password!")

    def _show_store_is_not_initialized_message(self) -> None:
        self._show_message(
            self._show_sign_up_screen, "Store is not initialized. Please sign up."
        )

    def _show_store_handle_screen(self) -> None:
        if self.app.store:
            screen = StoreHandleScreen(self.set_store)
            screen.styles.background = "black"
            self.app.pop_screen()
            self.app.install_screen(screen)
            self.app.push_screen(screen)
        else:
            raise StoreIsNotInitializedError("Store is not initialized!")

    def _show_store_initialized_message(self) -> None:
        def callback() -> None:
            self.app.pop_screen()
            self._show_store_handle_screen()

        self._show_message(callback, "You successfully initialized a store!")

    def _show_sign_up_screen(self) -> None:
        def callback(password: str) -> None:
            val = PasswordValidator(password).validate()

            if not val[0]:
                self._show_message(self._show_sign_up_screen, val[1])
                return

            self.app.store = store.try_initialize_store(password)
            self.app.pop_screen()
            self._show_store_initialized_message()

        signup_screen = SignUpScreen(callback)
        signup_screen.styles.background = "black"
        self.app.install_screen(signup_screen)
        self.app.push_screen(signup_screen)

    def set_store(self, password: str) -> None:
        try:
            logging.debug("Setting a store")
            self.app.store = store.try_initialize_existing_store(password)
        except StoreIsNotInitializedError:
            self._show_store_is_not_initialized_message()
            return

        if self.app.store:
            self._show_store_handle_screen()
        else:
            self._show_incorrect_password_message()
