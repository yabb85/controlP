from gi.repository import Gtk # type: ignore
from logging import debug as log_debug

# from .ampli import Ampli
from .headerbar import HeaderBar
from .menu import Menu
from .power import Power
from .source import Source


class ControlpWindow(Gtk.ApplicationWindow):
    def __init__(self, application, title):
        log_debug('initliaze window')
        super().__init__(application=application, title=title)
        self.set_default_size(800, 600)
        self._app = application

        self.hb = HeaderBar(self._app.props.coremodel)
        self.set_titlebar(self.hb)
        self._all = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self._power = Power(self._app.props.coremodel)
        self._power.props.visible = True
        self._all.pack_start(self._power, False, True, 0)
        self._command = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.source = Source(self._app.props.coremodel)
        self.source.props.visible = True
        self._command.pack_start(self.source, False, True, 0)
        self.menu = Menu(self._app.props.coremodel)
        self.menu.props.visible = True
        self._command.pack_start(self.menu, True, True, 0)
        self._command.props.visible = True
        self._all.pack_start(self._command, True, True, 0)
        self.add(self._all)
        self._all.show()
        log_debug('window initliazed')
