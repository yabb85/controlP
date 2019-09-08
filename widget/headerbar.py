from gi.repository import Gtk

from ..signal import get_player_signal


class HeaderBar(Gtk.HeaderBar):
    def __init__(self, stack):
        super().__init__()
        self.player = get_player_signal()

        box_left = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        ret = Gtk.Button()
        ret.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        ret.connect('clicked', self.on_ret_action)
        box_left.add(ret)
        self.pack_start(box_left)

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        self.set_custom_title(stack_switcher)
        self.set_show_close_button(True)

    def on_ret_action(self, button):
        self.player.emit('player-return-event')
