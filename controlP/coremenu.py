import asyncio
from threading import Thread
from logging import getLogger
from threading import RLock
from urllib.request import urlopen
from typing import List

from gi.repository import Gio, GObject # type: ignore
from gi.repository.GdkPixbuf import Pixbuf # type: ignore


LOGGER = getLogger(__name__)
log_debug = LOGGER.debug
SOUND_PIXBUF = Pixbuf.new_from_file_at_scale('controlP/music.png', 64, 64, True)


class RefreshPixbuf(Thread):
    def __init__(self, props, url):
        super().__init__()
        self.props = props
        self.url = url

    def run(self):
        log_debug('RefreshPixbuf run {}'.format(self.url))
        response = urlopen(self.url)
        if not response:
            return
        input_stream = Gio.MemoryInputStream.new_from_data(
            response.read(), None
        )
        if not input_stream:
            return
        self.props.pixbuf = Pixbuf.new_from_stream_at_scale(input_stream, 64, 64, True, None)
        return


class MenuModel(GObject.GObject):
    """
    Model used to display and item in menu list

    :param text: text displayed by item on list
    :param line_idx: line index in list
    :param url: url of picture displayed on list
    :param pixbuf:
    """

    text = GObject.Property(type=str)
    line_idx = GObject.Property(type=int)
    url = GObject.Property(type=str)
    pixbuf = GObject.Property(type=Pixbuf)
    thread = None

    def __init__(self, text, line_idx, url=None):
        super().__init__()
        self.props.text = text
        self.props.line_idx = line_idx
        self.props.url = url
        self.props.pixbuf = SOUND_PIXBUF
        self.thread = None
        if self.url:
            self.thread = RefreshPixbuf(self.props, self.props.url)
            self.thread.start()

    def update(self, text, line_idx, url=None):
        log_debug('MenuModel update text: {}, line_idx: {}, url: {}'.format(text, line_idx, url))
        self.props.text = text
        self.props.line_idx = line_idx
        if url and url != self.props.url:
            log_debug('with url: {}'.format(url))
            self.props.url = url
            if self.thread:
                if not self.thread.is_alive():
                    del self.thread
                else:
                    self.thread.join()
                    self.thread.url = self.props.url
            if not self.thread:
                self.thread = RefreshPixbuf(self.props, self.props.url)
            # log_debug('before: {}'.format(self.thread))
            # self.thread.join()
            # log_debug('after: {}'.format(self.thread))
            # self.thread = RefreshPixbuf(self.pixbuf, url)
            self.thread.start()
        elif not url:
            self.props.pixbuf = SOUND_PIXBUF


class CoreMenu(Gio.ListStore):
    """
    Model to display a menu list

    :param begin: is the index of first element displayed on menu
    :param end: is the index of last element displayed on menu
    :param total: is the number of element in list (not displayed)
    :param visible: the menu must be visible or not?
    :param up_visible: display button to display previous element in list
    :param down_visible: display button to display next element in list
    :param highlight: index of highlighted element
        (empty since use directory status instead of screen status)
    """

    begin = GObject.Property(type=int)
    end = GObject.Property(type=int)
    total = GObject.Property(type=int)
    visible = GObject.Property(type=bool, default=True)
    up_visible = GObject.Property(type=bool, default=True)
    down_visible = GObject.Property(type=bool, default=True)
    highlight = GObject.Property(type=int)
    items: List[MenuModel] = []

    def __init__(self):
        super().__init__()
        self.locker = RLock()
        self._previous_status = {}

    def update(self, status, visibility):
        log_debug('CoreMenu.update')
        log_debug('status: {}'.format(status))
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
            lines = status.get('lines', {})
            lines_size = len(lines)
            items_size = len(self.items)
            log_debug('lines_size: {}, items_size: {}'.format(lines_size, items_size))
            if items_size > lines_size:
                for i in range(items_size, lines_size, -1):
                    self.remove(i - 1)
                    self.items.pop()
                items_size = len(self.items)
            log_debug('lines_size: {}, items_size: {}'.format(lines_size, items_size))
            for key, value in lines.items():
                list_store_idx = key - 1
                log_debug('key: {}, value: {}'.format(key, value))
                text = value.get('value', None)
                index = value.get('begin_line', None)
                if not index:
                    index = list_store_idx + self.begin
                if value.get('highlight', 0) == 1:
                    self.highlight = index
                url = value.get('url', None)
                if list_store_idx < items_size:
                    self.items[list_store_idx].update(text, index, url)
                else:
                    row = MenuModel(text, index, url)
                    self.items.append(row)
                    self.append(row)
            items_size = len(self.items)
            log_debug('lines_size: {}, items_size: {}'.format(lines_size, items_size))
            self.up_visible = self.begin != 1
            self.down_visible = self.end != self.total
        self._previous_status = status
