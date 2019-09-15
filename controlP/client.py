import signal
import sys

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .application import Application
from .pioneer import Pioneer



def main():
    app = Application()
    app.run(sys.argv)


if __name__ == '__main__':
    main()
