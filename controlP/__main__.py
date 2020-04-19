import os
import sys
from logging import basicConfig

import gi  # type: ignore
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # type: ignore

from .application import Application
from .pioneer import Pioneer




def main():
    basicConfig(level=os.environ.get('LOGLEVEL', 'INFO'))
    app = Application()
    app.run(sys.argv)


if __name__ == '__main__':
    main()
