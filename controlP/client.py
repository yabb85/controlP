import os
import sys
from logging import basicConfig

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .application import Application
from .pioneer import Pioneer




def main():
    basicConfig(level=os.environ.get('LOGLEVEL', 'INFO'))
    app = Application()
    app.run(sys.argv)


if __name__ == '__main__':
    main()
