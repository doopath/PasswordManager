import json
import os
from pathlib import Path

from typing import Callable

import requests


class Settings:
    """
    A class used to manage application settings.

    Attributes
    ----------
    app_dir : str
        The directory where application stores its files.
    appdata_dir : str
        The directory where the application data is stored.
    settings_file : str
        The path to the settings file.
    settings : dict
        The application settings loaded from the settings file.

    Methods
    -------
    save()
        Saves the current settings to the settings file.
    restore_defaults()
        Restores the settings to their default values.
    _substitute_appdata(settings: dict) -> dict
        Substitutes the 'APPDATA' placeholder in the settings with the actual appdata directory.
    _get_settings() -> dict
        Loads the settings from the settings file.
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the Settings object.
        """
        self.app_dir: str = str(Path.home().joinpath("doopass"))
        self.appdata_dir: str = os.path.join(self.app_dir, "appdata")
        self.settings_file = os.path.join(self.appdata_dir, "settings.json")
        self._settings: dict
        self._initialize_settings()

    def save(self) -> None:
        """
        Saves the current settings to the settings file.
        """
        for pair in list(self._settings['local'].items()):
            self._settings['local'][pair[0]] = pair[1].replace(self.appdata_dir, 'APPDATA')

        with open(self.settings_file, mode="w", encoding="utf-8") as settings_file:
            json.dump(self._settings, settings_file, ensure_ascii=False, indent=4)

    def restore_defaults(self, callback: Callable = (lambda: ...)) -> None:
        """
        Restores the settings to their default values.
        """
        url = 'https://raw.githubusercontent.com/doopath/PasswordManager/master/default_config.json'
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f"Failed to download the default settings file. Status code: {response.status_code}")

        with open(self.settings_file, mode="w", encoding="utf-8") as settings:
            settings.write(json.dumps(response.json(), ensure_ascii=True, indent=4))
            callback()

        self._initialize_settings()

    def _initialize_settings(self) -> None:
        if not os.path.isdir(self.app_dir):
            os.mkdir(self.app_dir)

        if not os.path.isdir(self.appdata_dir):
            os.mkdir(self.appdata_dir)

        if not os.path.isfile(self.settings_file):
            self.restore_defaults()

        self._settings = self._substitute_appdata(self._get_settings())

    def _substitute_appdata(self, settings: dict) -> dict:
        """
        Substitutes the 'APPDATA' placeholder in the settings with the actual appdata directory.

        Parameters
        ----------
        settings : dict
            The settings to be modified.

        Returns
        -------
        dict
            The modified settings.
        """
        for pair in list(settings['local'].items()):
            value = pair[1]

            if 'APPDATA' in pair[1]:
                value = value.split('APPDATA')[1].split('/')[1]
                value = os.path.join(self.appdata_dir, value)

            settings['local'][pair[0]] = value

        return settings

    @property
    def settings(self) -> dict:
        return self._substitute_appdata(self._settings)

    def modify_property(self, section: str, key: str, value: str) -> dict:
        self._settings[section][key] = value
        self.save()

    def _get_settings(self) -> dict:
        """
        Loads the settings from the settings file.

        Returns
        -------
        dict
            The loaded settings.
        """
        with open(self.settings_file, mode="r", encoding="utf-8") as settings_file:
            settings = json.load(settings_file)

        return settings


config = Settings()
