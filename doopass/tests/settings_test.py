import unittest
import os
from pathlib import Path
from unittest.mock import patch
from doopass.core.settings import Settings


class TestSettingsInit(unittest.TestCase):
    def setUp(self):
        self.home_dir = "/home/doopath"
        self.app_dir = os.path.join(self.home_dir, "doopass")
        self.appdata_dir = os.path.join(self.app_dir, "appdata")
        self.settings_file = os.path.join(self.appdata_dir, "settings.json")

    @patch('pathlib.Path.home')
    def test_init_sets_app_dir(self, mock_home):
        mock_home.return_value = Path(self.home_dir)
        settings = Settings()
        self.assertEqual(settings.app_dir, self.app_dir)

    @patch('pathlib.Path.home')
    def test_init_sets_appdata_dir(self, mock_home):
        mock_home.return_value = Path(self.home_dir)
        settings = Settings()
        self.assertEqual(settings.appdata_dir, self.appdata_dir)

    @patch('pathlib.Path.home')
    def test_init_sets_settings_file(self, mock_home):
        mock_home.return_value = Path(self.home_dir)
        settings = Settings()
        self.assertEqual(settings.settings_file, self.settings_file)

    @patch('pathlib.Path.home')
    @patch('doopass.core.settings.Settings._get_settings')
    def test_init_calls_get_settings(self, mock_get_settings, mock_home):
        mock_home.return_value = Path(self.home_dir)
        settings = Settings()
        mock_get_settings.assert_called_once()

    @patch('pathlib.Path.home')
    @patch('doopass.core.settings.Settings._get_settings')
    @patch('doopass.core.settings.Settings._substitute_appdata')
    def test_init_sets_settings(self, mock_substitute_appdata, mock_get_settings, mock_home):
        mock_home.return_value = Path(self.home_dir)
        mock_get_settings.return_value = {'local': {'key': 'value'}}
        mock_substitute_appdata.return_value = {'local': {'key': 'value'}}
        settings = Settings()
        self.assertEqual(settings.settings, {'local': {'key': 'value'}})


if __name__ == '__main__':
    unittest.main()