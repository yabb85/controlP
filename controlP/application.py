from threading import Event, Thread, Timer
from time import sleep

from gi.repository import Gio, GObject, Gtk

from .coremodel import CoreModel
from .widget.window import ControlpWindow as Window

MENU_XML = """
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <menu id="app-menu">
    <section>
      <item>
        <attribute name="action">app.about</attribute>
        <attribute name="label" translatable="yes">_About</attribute>
      </item>
      <item>
        <attribute name="action">app.quit</attribute>
        <attribute name="label" translatable="yes">_Quit</attribute>
        <attribute name="accel">&lt;Primary&gt;q</attribute>
    </item>
    </section>
  </menu>
</interface>
"""


class RefreshScreen(Thread):
    def __init__(self, coremodel, duration=1.0):
        super().__init__()
        self._coremodel = coremodel
        self._stop = Event()
        self.duration = duration

    def run(self):
        while not self._stop.wait(self.duration):
            self._coremodel.do_network_player_screen_get_status_event()

    def cancel(self):
        self._stop.set()


class Application(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            application_id="org.toto",
            flags=Gio.ApplicationFlags.FLAGS_NONE,
            **kwargs
        )
        self._window = None
        self._coremodel = CoreModel()
        self._screen_refresh = RefreshScreen(self._coremodel, 5.0)

    @GObject.Property(type=CoreModel, flags=GObject.ParamFlags.READABLE)
    def coremodel(self):
        return self._coremodel

    @GObject.Property(type=Window, flags=GObject.ParamFlags.READABLE)
    def window(self):
        return self._window

    def quit(self, action=None, param=None):
        if self._window:
            self._window.destroy()

    def do_startup(self):
        Gtk.Application.do_startup(self)

        action = Gio.SimpleAction.new('about', None)
        action.connect('activate', self.on_about)
        self.add_action(action)

        action = Gio.SimpleAction.new('quit', None)
        action.connect('activate', self.on_quit)
        self.add_action(action)

        builder = Gtk.Builder.new_from_string(MENU_XML, -1)
        self.set_app_menu(builder.get_object('app-menu'))

    def do_shutdown(self):
        self._screen_refresh.cancel()
        Gtk.Application.do_shutdown(self)

    def do_activate(self):
        if not self._window:
            self._window = Window(application=self, title="controlP")
        self._window.present()
        self._screen_refresh.start()

    def on_about(self, action, param):
        about_dialog = Gtk.AboutDialog(transient_for=self.window, modal=True)
        about_dialog.present()

    def on_quit(self, action, param):
        self.quit()
