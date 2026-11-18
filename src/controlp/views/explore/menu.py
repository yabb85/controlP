from itertools import zip_longest
from math import floor
from pathlib import Path

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ListProperty, ObjectProperty, StringProperty, NumericProperty
from kivymd.uix.list import MDListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.font_definitions import fonts
from kivymd.uix.button import MDButtonIcon
from kivymd.uix.recycleview import MDRecycleView
from kivymd.uix.boxlayout import MDBoxLayout


class MenuItem(MDListItem):
    text = StringProperty()
    index = NumericProperty()
    url = StringProperty()

    def on_release(self, **kwargs):
        # self.parent.parent.parent.explore(self.index)
        self.parent.parent.explore(self.index)


class MenuView(MDRecycleView):
    controller = ObjectProperty()
    model = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        """
        Use this call because model and controller are not set during __init__ call
        """
        super().on_kv_post(base_widget)
        self.model.add_observer(self)

    def explore(self, index: int):
        """
        open item to explore tree
        """
        self.controller.explore_set(index)

    def explore_down(self):
        """
        Removed with new infinity list
        """
        self.controller.explore_down()

    def explore_up(self):
        """
        Removed with new infinity list
        """
        self.controller.explore_up()

    def model_is_changed(self):
        """
        Refresh view and move scroll view to active item
        """
        self.data = self.model.get_data()
        shift = self.height / dp(56) - 1 # retirer une ligne pour avoir la reference en haut de l'item plutot qu'en bas
        shifted = self.model.total_line - shift
        select = self.model.selected_line - 1
        total = self.model.total_line - 1
        self.scroll_y = 1 - (select / (total - shift))


Builder.load_file(str(Path(__file__).parent.joinpath('menu.kv')))
