"""
Model used by explore view
"""
from enum import Enum


class PreloadStatus(Enum):
    PRELOAD = 1
    LOAD = 2
    NONE = 3


class ExploreModel:
    observers: list = []
    nb_lines: int = 0
    first_line: int = 0
    last_line: int = 0
    total_line: int = 0
    selected_line: int = 0
    up_visible: bool = False
    down_visible: bool = False
    lines: list = []
    top: str= "0"
    scroll_reset: bool = False
    cache: dict = {}
    title: str = ''

    def load(self, status):
        """
        Load menu with first item displayed in view
        """
        self.nb_lines = status['nb_lines']
        self.first_line = status['begin_disp']
        self.last_line = status['end_disp']
        self.total_line = status['total_line']
        self.lines = status.get('lines', {})
        self.up_visible = self.first_line != 1
        self.down_visible = self.last_line != self.total_line
        self.top = status.get('top', '0')
        self.title = status.get('title', '')
        if self.title:
            plop = {}
            for key, value in status.get('lines').items():
                plop[value['begin_line']] = value
            self.cache.setdefault(self.title, {})
            self.cache[self.title].update(plop)
        self.notify_observers()

    def get_data(self):
        data = [{'text': elt['value'], 'index': key, 'url': elt['url']} for key, elt in self.cache[self.title].items()]
        return data

    def preload_update(self, new_lines):
        """
        add preload data in cache to have all item in menu view
        """
        plop = {}
        for key, value in new_lines.items():
            line = {
                'begin_line': value['begin_line'],
                'value': value['value'],
                'url': value['url'],
                'load': 0
            }
            plop.setdefault(value['begin_line'], line)
            plop[value['begin_line']]['load'] += 1
        self.last_line = max(self.cache[self.title])
        self.first_line = min(self.cache[self.title])
        self.cache[self.title].update(plop)
        self.cache[self.title] = dict(sorted(self.cache[self.title].items()))

    def get_preload_status(self):
        """
        returne if preload is needed
        """
        # status = PreloadStatus.NONE
        # if not self.title:
            # status = PreloadStatus.LOAD
        # elif self.title not in self.cache:
            # status = PreloadStatus.LOAD
        # elif self.total_line != len(self.cache[self.title]):
            # status = PreloadStatus.PRELOAD
        return self.total_line != len(self.cache[self.title])

    def set_selected_line(self, line):
        """
        Set current line selected in player screen
        Used to set scroll view
        """
        self.selected_line = line

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.model_is_changed()
