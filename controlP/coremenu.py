from threading import RLock

from gi.repository import Gio, GObject


class MenuModel(GObject.GObject):
    """
    """

    text = GObject.Property(type=str)
    line_idx = GObject.Property(type=int)

    def __init__(self, text, line_idx):
        super().__init__()
        self.props.text = text
        self.props.line_idx = line_idx


class CoreMenu(Gio.ListStore):
    """
    """

    begin = GObject.Property(type=int)
    end = GObject.Property(type=int)
    total = GObject.Property(type=int)
    visible = GObject.Property(type=bool, default=True)
    up_visible = GObject.Property(type=bool, default=True)
    down_visible = GObject.Property(type=bool, default=True)
    highlight = GObject.Property(type=int)

    def __init__(self):
        super().__init__()
        self.locker = RLock()
        self._previous_status = {}

    def update(self, status, visibility):
        self.visible = visibility
        if not self.visible or not status:
            return
        shared_items = {
            k: status[k]
            for k in status
            if k in self._previous_status and status[k] == self._previous_status[k]
        }
        if self._previous_status and len(shared_items) == len(self._previous_status):
            return
        with self.locker:
            self.begin = status.get('begin_disp', 0)
            self.end = status.get('end_disp', 0)
            self.total = status.get('total_line', 0)
            self.remove_all()
            lines = status.get('lines', {})
            for key, value in lines.items():
                text = value.get('value', None)
                index = key + self.begin - 1
                # if value.get('highlight', '0') == '1':
                    # self.highlight = index
                row = MenuModel(text, index)
                self.append(row)
            self.up_visible = self.begin != 1
            self.down_visible = self.end != self.total
        self._previous_status = status
