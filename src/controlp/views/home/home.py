from pathlib import Path

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from controlp import __path__ as package_path
from pathlib import Path


DATA_DIR = Path(package_path[0]).joinpath('data')


class HomeDeviceCard(MDCard):
    name = StringProperty()
    image_path = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_press(self, **kwargs):
        self.parent.parent.parent.choose(self.name)


class HomeView(MDScreen):
    controller = ObjectProperty()
    model = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_is_changed()
        self.model.add_observer(self)

    def android_back_click(self, window, key, *args):
        if key == 27:
            return True

    def on_enter(self):
        Window.bind(on_keyboard=self.android_back_click)

    def on_leave(self):
        Window.unbind(on_keyboard=self.android_back_click)

    def choose(self, name: str):
        self.controller.choose(name)

    def model_is_changed(self):
        self.ids.home_layout.clear_widgets()
        for name, device in self.model.devices.items():
            model = device.model.split('/')[0]
            image_path = DATA_DIR.joinpath('images', f'{model}.jpg')
            self.ids.home_layout.add_widget(
                HomeDeviceCard(name=device.friendly_name, image_path=str(image_path))
            )
        self.ids.home_layout.add_widget(MDLabel())


Builder.load_file(str(Path(__file__).parent.joinpath('home.kv')))
