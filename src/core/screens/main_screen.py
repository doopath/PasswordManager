from typing import Any, Callable

from .. import store
from ..exceptions import StoreIsNotInitializedError
from ..password_validation import PasswordValidator
from .main_menu_screen import MainMenuScreen
from .message_screen import MessageScreen
from .screen import Screen
from .sign_up_screen import SignUpScreen


class MainScreen(Screen):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def on_mount(self) -> None:
        screen = MainMenuScreen(set_store=self.set_store, app=self.app)
        self.screen.styles.background = "black"
        self.app.install_screen(screen)
        self.app.push_screen(screen)

    def show_message(self, callback: Callable[[], Any], text: str) -> None:
        message_screen = MessageScreen(callback, text)
        self.app.install_screen(message_screen)
        self.app.push_screen(message_screen)

    def show_incorrect_password_message(self) -> None:
        self.show_message(self.app.pop_screen, "Incorrect password!")

    def show_store_is_not_initialized_message(self) -> None:
        self.show_message(
            self.show_sign_up_screen, "Store is not initialized. Please sign up."
        )

    def show_store_handle_screen(self) -> None:
        pass

    def show_store_initialized_message(self) -> None:
        def callback() -> None:
            self.app.pop_screen()
            self.show_store_handle_screen()

        self.show_message(callback, "You successfully initialized a store!")

    def show_sign_up_screen(self) -> None:
        def callback(password: str) -> None:
            val = PasswordValidator(password).validate()

            if not val[0]:
                self.show_message(self.show_sign_up_screen, val[1])
                return

            self.app.store = store.try_initialize_store(password)
            self.app.pop_screen()
            self.show_store_initialized_message()

        signup_screen = SignUpScreen(callback)
        self.app.pop_screen()
        self.app.install_screen(signup_screen)
        self.app.push_screen(signup_screen)

    def set_store(self, password: str) -> None:
        try:
            self.app.store = store.try_initialize_existing_store(password)
        except StoreIsNotInitializedError:
            self.show_store_is_not_initialized_message()
            return

        if self.app.store:
            ...
            # show StoreHandleScreen
        else:
            self.show_incorrect_password_message()
