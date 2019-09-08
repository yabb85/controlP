import gi
from gi.repository import Gtk

from .pioneer import Pioneer
from .widget.window import PioneerWindow

gi.require_version('Gtk', '3.0')



def main():
    window = PioneerWindow()
    window.connect('destroy', Gtk.main_quit)
    window.show_all()
    Gtk.main()


if __name__ == '__main__':
    main()
