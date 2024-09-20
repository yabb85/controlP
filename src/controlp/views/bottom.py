from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty
from kivymd.uix.floatlayout import MDFloatLayout
from pathlib import Path


class BottomView(MDFloatLayout):
    amplifier_controller = ObjectProperty()
    amplifier_model = ObjectProperty()
    bottom_controller = ObjectProperty()
    bottom_model = ObjectProperty()
    active = BooleanProperty(False)
    screen = StringProperty()

    # def __init__(self, **kwargs):
        # super().__init__(*kwargs)

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.amplifier_model.add_observer(self)
        self.bottom_model.add_observer(self)
        Clock.schedule_once(self.load)

    def open_window(self):
        self.amplifier_controller.open_window()

    def vol_down(self):
        self.amplifier_controller.vol_down()

    def vol_up(self):
        self.amplifier_controller.vol_up()

    def current_play(self):
        self.bottom_controller.current_play()

    def load(self, dt):
        self.amplifier_controller.load()

    def model_is_changed(self):
        print('bottom model_is_changed:', str(self.bottom_model.screen))
        self.active = self.amplifier_model.active
        self.screen = self.bottom_model.screen


Builder.load_file(str(Path(__file__).parent.joinpath('bottom.kv')))
