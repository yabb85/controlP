from pathlib import Path

from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivymd.uix.stacklayout import MDStackLayout


REPEAT = {
    0: 'repeat-off',
    1: 'repeat-once',
    2: 'repeat',
}

SHUFFLE = {
    0: 'shuffle-disabled',
    1: 'shuffle',
}

PLAY = {
    0: 'play',
    1: 'play',
    2: 'pause',
}

class ControlView(MDStackLayout):
    controller = ObjectProperty()
    model = ObjectProperty()
    icon_repeat = StringProperty()
    icon_shuffle = StringProperty()
    icon_play = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.icon_repeat = REPEAT[0]
        self.icon_shuffle = SHUFFLE[0]

    def on_kv_post(self, base_widget):
        """
        Use this call because model and controller are not set during __init__ call
        """
        super().on_kv_post(base_widget)
        self.model.add_observer(self)

    def previous(self):
        self.controller.previous()

    def play_pause(self):
        self.controller.play_pause()

    def next(self):
        self.controller.next()

    def shuffle(self):
        self.controller.shuffle()

    def repeat(self):
        self.controller.repeat()

    def model_is_changed(self):
        self.icon_repeat = REPEAT[self.model.repeat]
        self.icon_shuffle = SHUFFLE[self.model.shuffle]
        self.icon_play = PLAY[self.model.play]


Builder.load_file(str(Path(__file__).parent.joinpath('control.kv')))
