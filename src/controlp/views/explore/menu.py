from itertools import zip_longest
from pathlib import Path

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ListProperty, ObjectProperty, StringProperty, NumericProperty
from kivymd.uix.list import MDListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.font_definitions import fonts
from kivymd.uix.button import MDButtonIcon


class MenuItem(MDListItem):
    text = StringProperty()
    index = NumericProperty()
    url = StringProperty()

    def on_release(self, **kwargs):
        self.parent.parent.parent.explore(self.index)


class MenuView(MDScrollView):
    controller = ObjectProperty()
    model = ObjectProperty()
    items = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        """
        Use this call because model and controller are not set during __init__ call
        """
        super().on_kv_post(base_widget)
        self.model.add_observer(self)

    def explore(self, index: int):
        self.controller.explore_set(index)

    def explore_down(self):
        self.controller.explore_down()

    def explore_up(self):
        self.controller.explore_up()

    def model_is_changed(self):
        temporary_list = []
        for item, status_item in zip_longest(self.items, sorted(self.model.lines.items())):
            temporary_list.append((item, status_item))
        # self.ids.menu_up.clear_widgets()
        self.display_button_up()
        for item, status_item in temporary_list:
            if item and status_item:
                if item.text != status_item[1]['value']:
                    item.text = status_item[1]['value']
                    item.index = status_item[1]['begin_line']
                if item.url != status_item[1].get('url', ''):
                    item.url = status_item[1].get('url', '')
            elif item and not status_item:
                self.ids.menu_list.remove_widget(item)
                self.items.remove(item)
            elif status_item and not item:
                item = MenuItem(text=status_item[1]['value'], index=status_item[1]['begin_line'], url=status_item[1].get('url', ''))
                self.ids.menu_list.add_widget(item)
                self.items.append(item)
            # self.ids.menu_list.clear_widgets()
            # for index, status_item in sorted(self.model.lines.items()):
                # item = MenuItem(text=status_item['value'], index=int(index), url=status_item.get('url', ''))
                # self.ids.menu_list.add_widget(item)
        self.display_button_down()
        if self.model.scroll_reset:
            self.scroll_to(self.items[0])

    def display_button_up(self):
        if self.model.up_visible:
            menu_up = self.ids.menu_up
            menu_up.height = dp(50)
            menu_up.opacity = 1
            menu_up.disabled = False
            button = self.ids.button_up
            button.height = dp(50)
            button.opacity = 1
            button.disabled = False
        else:
            menu_up = self.ids.menu_up
            menu_up.height = 0
            menu_up.opacity = 0
            menu_up.disabled = True
            button = self.ids.button_up
            button.height = 0
            button.opacity = 0
            button.disabled = True

    def display_button_down(self):
        if self.model.down_visible:
            menu_down = self.ids.menu_down
            menu_down.height = dp(50)
            menu_down.opacity = 1
            menu_down.disabled = False
            button = self.ids.button_down
            button.height = dp(50)
            button.opacity = 1
            button.disabled = False
        else:
            menu_down = self.ids.menu_down
            menu_down.height = 0
            menu_down.opacity = 0
            menu_down.disabled = True
            button = self.ids.button_down
            button.height = 0
            button.opacity = 0
            button.disabled = True

Builder.load_file(str(Path(__file__).parent.joinpath('menu.kv')))
