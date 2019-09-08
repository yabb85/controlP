from json import loads
from logging import debug as log_debug
from logging import error as log_error

from gi.repository import Gtk

from ..signal import get_player_signal
from .utils import ListBoxRowSource


class Cover(Gtk.Box):
    """
    Widget to display title read on player
    """

    def __init__(self, data):
        super().__init__()
        self.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.player = get_player_signal()

        infos = Gtk.Box()
        self.pack_start(infos, True, True, 0)
        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
        infos.pack_start(self.listbox, True, True, 0)

        for index, line in data['lines'].items():
            row = ListBoxRowSource(line['value'], index)
            row.set_selectable(False)
            self.listbox.add(row)

        cover = Gtk.Box()
        self.pack_start(cover, True, True, 0)
        self.show_all()


class MenuList(Gtk.Box):
    """
    Widget to display menu
    """

    def __init__(self, data):
        super().__init__()
        self.player = get_player_signal()
        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.begin_disp = int(data['begin_disp'])
        self.end_disp = int(data['end_disp'])
        self.total_lines = int(data['total_line'])

        up = Gtk.Button()
        up.add(Gtk.Arrow(Gtk.ArrowType.UP, Gtk.ShadowType.NONE))
        up.connect('clicked', self.on_up_activated)
        if self.begin_disp != 1:
            up.show_all()
        else:
            up.hide()
        up.set_size_request(-1, 50)

        self.pack_start(up, False, False, 0)
        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.listbox.connect('row-activated', self.on_row_activated)
        self.listbox.show_all()
        self.pack_start(self.listbox, True, True, 0)

        down = Gtk.Button()
        down.add(Gtk.Arrow(Gtk.ArrowType.DOWN, Gtk.ShadowType.NONE))
        down.connect('clicked', self.on_down_activated)
        if self.end_disp != self.total_lines:
            down.show_all()
        else:
            down.hide()
        down.set_size_request(-1, 50)
        self.pack_start(down, False, False, 0)
        self.show()

        for index, line in data['lines'].items():
            row = ListBoxRowSource(line['value'], self.begin_disp + int(index) - 1)
            row.show_all()
            self.listbox.add(row)

    def on_row_activated(self, listbox, row):
        self.player.emit('player-set-line-event', int(row.value))

    def on_up_activated(self, button):
        self.player.emit('player-select-line-event', self.begin_disp - 8)

    def on_down_activated(self, button):
        self.player.emit('player-select-line-event', self.end_disp + 1)


class Menu(Gtk.Box):
    def __init__(self):
        super().__init__()
        self.player = get_player_signal()
        self.player.connect('player-screen-status-event', self.on_screen_update)
        self.child = None

    def on_screen_update(self, signal, value):
        """
        Refresh view when screen is updated
        """
        log_debug('on_screen_update {}'.format(value))
        val = loads(value)
        if self.child:
            self.child.destroy
            self.remove(self.child)
        if 'type' in val and val['type'] == '01':
            self.child = MenuList(val)
            self.pack_start(self.child, True, True, 0)
        elif 'type' in val and val['type'] == '02':
            self.child = Cover(val)
            self.pack_start(self.child, True, True, 0)
        else:
            log_error(val)
            self.player.emit('player-screen-get-status-event')
