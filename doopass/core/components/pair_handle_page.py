from textual.containers import Grid, Vertical
from textual.widget import Widget
from textual.widgets import Button, Label, Input


class PairHandlePageCustomization:
    def __init__(self, **kwargs):
        self.key = kwargs['key'] if 'key' in kwargs else ''
        self.value = kwargs['value'] if 'value' in kwargs else ''
        self.button_text = kwargs['button_text'] if 'button_text' in kwargs else 'Submit'
        self.key_label = kwargs['key_label'] if 'key_label' in kwargs else 'Key'
        self.value_label = kwargs['value_label'] if 'value_label' in kwargs else 'Value'


class PairHandlePage:
    def __init__(self, custom: PairHandlePageCustomization = PairHandlePageCustomization()) -> None:
        self.custom = custom
        self.key_input_field_id = "pair_update_key_input"
        self.password_input_field_id = "pair_update_password_input"
        self.update_button_id = "pair_update_button"
        self.back_button_id = "pair_back_button"

    def create(self) -> Widget:
        return Vertical(
            Grid(
                Grid(
                    Label(f"{self.custom.key_label}:", classes="store_pair_update_label"),
                    classes="store_pair_update_label_container",
                ),
                Input(
                    value=self.custom.key,
                    classes="store_pair_update_key_input store_pair_update_input input_field",
                    id=self.key_input_field_id,
                ),
                classes="store_pair_update_attribute_container",
            ),
            Grid(
                Grid(
                    Label(f"{self.custom.value_label}:", classes="store_pair_update_label"),
                    classes="store_pair_update_label_container",
                ),
                Input(
                    value=self.custom.value,
                    classes="store_pair_update_password_input store_pair_update_input input_field",
                    id=self.password_input_field_id,
                ),
                classes="store_pair_update_attribute_container",
            ),
            Grid(
                Button(
                    self.custom.button_text,
                    classes="store_pair_update_button button",
                    id=self.update_button_id,
                ),
                Button(
                    "Back",
                    classes="store_pair_update_button button",
                    id=self.back_button_id,
                ),
                classes="store_pair_update_buttons_container",
            ),
            classes="store_pair_update_container",
        )
