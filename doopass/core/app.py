import logging
import os

from textual import app
from .settings import config
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
            filename=config.settings['local']['log_file'],
            level=logging.INFO,
            filemode="a",
            format="%(asctime)s %(levelname)s %(message)s",
        )

    def _init_appdir(self) -> None:
        if not os.path.exists(config.app_dir):
            logging.debug("Creating the app directory")
            os.mkdir(config.app_dir)
            logging.debug("The app directory has been created")
