from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Label, Header, Static
from textual import events
from textual.containers import Vertical, Horizontal


class HelpScreen(Screen):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, id="header")
        yield Vertical(
            Vertical(
                Vertical(
                    Label("Help Screen", classes="help_screen_title"),
                    classes="help_screen_title_container",
                ),
                # HOTKEYS
                Label("> Hotkeys <", classes="help_screen_items_title"),
                Horizontal(
                    Label("Q", classes="help_screen_label_key"),
                    Label(" or ", classes="help_screen_label_key"),
                    Label("ESCAPE", classes="help_screen_label_key"),
                    Label(" - quit the app", classes="help_screen_label_description"),
                    classes="help_screen_label_container",
                ),
                Horizontal(
                    Label("SPACE", classes="help_screen_label_key"),
                    Label(
                        " - leave help screen", classes="help_screen_label_description"
                    ),
                    classes="help_screen_label_container",
                ),
                Horizontal(
                    Label("H", classes="help_screen_label_key"),
                    Label(
                        " - open help screen", classes="help_screen_label_description"
                    ),
                    classes="help_screen_label_container",
                ),
                Horizontal(
                    Label("DownArrow", classes="help_screen_label_key"),
                    Label(" or ", classes="help_screen_label_key"),
                    Label("TAB", classes="help_screen_label_key"),
                    Label(" or ", classes="help_screen_label_key"),
                    Label("J", classes="help_screen_label_key"),
                    Label(
                        " - focus next element",
                        classes="help_screen_label_description",
                    ),
                    classes="help_screen_label_container",
                ),
                Horizontal(
                    Label("UpArrow", classes="help_screen_label_key"),
                    Label(" or ", classes="help_screen_label_key"),
                    Label("Shift+TAB", classes="help_screen_label_key"),
                    Label(" or ", classes="help_screen_label_key"),
                    Label("K", classes="help_screen_label_key"),
                    Label(
                        " - focus previous element",
                        classes="help_screen_label_description",
                    ),
                    classes="help_screen_label_container",
                ),
                Vertical(
                    Label(
                        "Register of the key pressed doesn't matter,",
                        classes="help_screen_label_comment",
                    ),
                    Label(
                        "but be sure you are using english keyboard layout.",
                        classes="help_screen_label_comment",
                    ),
                    classes="help_screen_comment_container",
                ),
                Static(classes="help_screen_separator"),
                # ABOUT
                Label("> About Doopass <", classes="help_screen_items_title"),
                Horizontal(
                    Label(
                        "This software is ABSOLUTELY FREE and open-source.",
                        classes="help_screen_label_description",
                    ),
                    classes="help_screen_label_container",
                ),
                Horizontal(
                    Label(
                        "See LICENSE file for more information.",
                        classes="help_screen_label_description",
                    ),
                    classes="help_screen_label_container",
                ),
                Horizontal(
                    Label("Github: ", classes="help_screen_label_description"),
                    Label(
                        "https://github.com/doopath/PasswordManager",
                        classes="help_screen_label_link",
                    ),
                    classes="help_screen_label_container",
                ),
                Horizontal(
                    Label("Contact me: ", classes="help_screen_label_description"),
                    Label(
                        "doopath@gmail.com",
                        classes="help_screen_label_highlight",
                    ),
                    classes="help_screen_label_container",
                ),
                Horizontal(
                    Label("Contact me: ", classes="help_screen_label_description"),
                    Label(
                        "https://t.me/doopath",
                        classes="help_screen_label_link",
                    ),
                    classes="help_screen_label_container",
                ),
                classes="help_screen_container",
            ),
            classes="help_screen_supercontainer",
        )

    def on_key(self, event: events.Key) -> None:
        if event.key == "space":
            event.stop()
            self.app.pop_screen()
