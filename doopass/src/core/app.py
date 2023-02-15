import logging
import os

from textual import app
from textual.screen import Screen

from . import constants
from .store import Store


class App(app.App):
    CSS_PATH = "../assets/styles.css"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.store: Store | None
        self._init_appdir()
        self._setup_logging()

    def _setup_logging(self) -> None:
        logging.basicConfig(
            filename=constants.LOG_FILE,
            level=logging.DEBUG,
            filemode="a",
            format="%(asctime)s %(levelname)s %(message)s",
        )

    def _init_appdir(self) -> None:
        if not os.path.exists(constants.APP_DIR):
            logging.debug("Creating the app directory")
            os.mkdir(constants.APP_DIR)
            logging.debug("The app directory has been created")

    def apply_screen(
        self, screen: Screen, pop: bool = True, name: str | None = None
    ) -> None:
        ...
