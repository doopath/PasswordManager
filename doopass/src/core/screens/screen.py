from textual import screen
from textual import events
from ..app import App
from .help_screen import HelpScreen


class Screen(screen.Screen):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.app: App

    def on_key(self, event: events.Key) -> None:
        match event.key.lower():
            case "tab" | "down" | "j":
                event.stop()
                self.screen.focus_next(selector="*")
            case "shift+tab" | "up" | "k":
                event.stop()
                self.screen.focus_previous(selector="*")
            case "h":
                event.stop()
                self.app.apply_screen(HelpScreen(), pop=False)
            case "escape" | "q":
                event.stop()
                self.app.exit()

    def on_paste(self, event: events.Paste) -> None:
        event.stop()
