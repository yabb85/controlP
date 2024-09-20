from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, ColorProperty, ListProperty
from kivy.core.window import Window
from kivymd.uix.appbar import MDTopAppBar
from pathlib import Path


class TopView(MDTopAppBar):
    controller = ObjectProperty()
    model = ObjectProperty()
    friendly_name = StringProperty()
    power_status = ColorProperty()
    items = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        """
        Use this call because model and controller are not set during __init__ call
        """
        super().on_kv_post(base_widget)
        self.model.add_observer(self)

    def power(self):
        self.controller.power()

    def model_is_changed(self):
        self.friendly_name = self.model.device.friendly_name
        power_status = self.model.power_status == 'PWR0'
        self.power_status = self.theme_cls.primaryColor if power_status else self.theme_cls.disabledTextColor


Builder.load_file(str(Path(__file__).parent.joinpath('top.kv')))
