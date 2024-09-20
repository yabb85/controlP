from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ObjectProperty, ListProperty
from kivymd.uix.list import MDListItem
from kivymd.uix.scrollview import MDScrollView
from pathlib import Path


class InputItem(MDListItem):
    text = StringProperty()
    code = NumericProperty()
    active = BooleanProperty()

    def on_press(self, **kwargs):
        self.parent.parent.choose_input(self.code)


class InputListView(MDScrollView):
    controller = ObjectProperty()
    model = ObjectProperty()
    items = ListProperty()

    def __init__(self, **kwargs):
        """
        Warning if instanciated with kv file the kwargs is empty.
        Use on_kv_post instead
        """
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        """
        Use this call because model and controller are not set during __init__ call
        """
        super().on_kv_post(base_widget)
        self.model.add_observer(self)
        for key, value in self.model._sources.items():
            item = InputItem(
                text=value,
                code=key,
                active=False
            )
            self.ids.input_list.add_widget(item)
            self.items.append(item)

    def choose_input(self, code):
        self.controller.choose_input(code)

    def model_is_changed(self):
        power_status = self.model.power_status == 'PWR0'
        self.power_status = 'orange' if power_status else 'grey'
        for item in self.items:
            item.active = (item.code == self.model.input_status) and power_status


Builder.load_file(str(Path(__file__).parent.joinpath('input_list.kv')))
