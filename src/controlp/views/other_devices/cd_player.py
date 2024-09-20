from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty, BooleanProperty, ColorProperty

from pathlib import Path


class CDPlayerLayout(MDBoxLayout):
    controller = ObjectProperty()
    model = ObjectProperty()
    active = BooleanProperty(False)
    button_color = ColorProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        """
        Use this call because model and controller are not set during __init__ call
        """
        super().on_kv_post(base_widget)
        self.model.add_observer(self)

    def set_active(self, switch_instance):
        self.controller.set_active(switch_instance.active)

    def model_is_changed(self):
        self.active = self.model.get_active()
        if self.active:
            self.button_color = self.theme_cls.onSurfaceColor
        else:
            self.button_color = self.theme_cls.disabledTextColor


Builder.load_file(str(Path(__file__).parent.joinpath('cd_player.kv')))
