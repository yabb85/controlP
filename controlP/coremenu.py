from gi.repository import Gio, GObject


class MenuModel(GObject.GObject):
    """
    """

    text = GObject.Property(type=str)
    line_idx = GObject.Property(type=str)

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

    def __init__(self):
        super().__init__()

    def update(self, status, visibility):
        self.visible = visibility
        if self.visible and status:
            self.remove_all()
            self.begin = int(status.get('begin_disp', None))
            self.end = int(status.get('end_disp', None))
            self.total = int(status.get('total_line', None))
            lines = status.get('lines', {})
            for key, value in lines.items():
                text = value.get('value', None)
                row = MenuModel(text, key)
                self.append(row)
            self.up_visible = self.begin != 1
            self.down_visible = self.end != self.total
