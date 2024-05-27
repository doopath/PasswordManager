import base64

from textual.app import ComposeResult
from textual.containers import Vertical, Grid
from textual.widgets import Label, Button
from ..settings import config


class SettingsPairsList(Vertical):
    def __init__(self, section: str, title: str, *args, **kwargs):
        kwargs['classes'] = "settings_manage_page_pairs_container"
        super().__init__(*args, **kwargs)
        self.section = section
        self.title = title

    def compose(self) -> ComposeResult:
        yield Label(
            self.title,
            classes="settings_manage_page_pairs_label"
        )

        for pair in config.settings[self.section].items():
            key = base64.b16encode(pair[0].encode()).decode()
            section = base64.b16encode(self.section.encode()).decode()

            yield Grid(
                Label(
                    pair[0],
                    classes="settings_manage_page_pair_label_first"
                ),
                Label(
                    pair[1],
                    classes="settings_manage_page_pair_label_second"
                ),
                Button(
                    "Change",
                    classes="settings_manage_page_pair_button button",
                    id=f"CHANGE_SETTING_BUTTON-KEY_{key}_{section}"
                ),
                classes="settings_manage_page_pair_container"
            )
