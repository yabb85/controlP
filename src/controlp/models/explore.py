

class ExploreModel:
    observers: list = []
    nb_lines: int = 0
    first_line: int = 0
    last_line: int = 0
    total_line: int = 0
    up_visible: bool = False
    down_visible: bool = False
    lines: list = []
    top: str= "0"
    scroll_reset: bool = False

    def load(self, status):
        self.nb_lines = status['nb_lines']
        self.first_line = status['begin_disp']
        self.last_line = status['end_disp']
        self.total_line = status['total_line']
        self.lines = status.get('lines', {})
        self.up_visible = self.first_line != 1
        # if self.up_visible:
            # self.lines[0] = {
                # 'begin_disp': 0,
                # 'begin_line': 0,
                # 'size_value': 1,
                # 'value': '^',
                # 'size_url': 0,
                # 'url': ''
            # }
        self.down_visible = self.last_line != self.total_line
        # if self.down_visible:
            # self.lines[self.total_line + 1] = {
                # 'begin_disp': self.total_line + 1,
                # 'begin_line': self.total_line + 1,
                # 'size_value': 1,
                # 'value': 'v',
                # 'size_url': 0,
                # 'url': ''
            # }
        self.top = status.get('top', '0')
        self.notify_observers()

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.model_is_changed()
