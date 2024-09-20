from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty, BooleanProperty, ColorProperty
from kivymd.uix.boxlayout import MDBoxLayout
from pathlib import Path


class AmplifierLayout(MDBoxLayout):
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

    def start_stop_amplifier(self):
        self.controller.start_stop_amplifier()

    def change_input(self):
        self.controller.change_input()

    def vol_down(self):
        self.controller.vol_down()

    def vol_up(self):
        self.controller.vol_up()

    def model_is_changed(self):
        self.active = self.model.get_active()
        if self.active:
            self.button_color = self.theme_cls.onSurfaceColor
        else:
            self.button_color = self.theme_cls.disabledTextColor


Builder.load_file(str(Path(__file__).parent.joinpath('amplifier.kv')))
