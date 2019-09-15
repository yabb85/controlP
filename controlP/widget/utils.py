from gi.repository import Gtk


class ListBoxRowSource(Gtk.ListBoxRow):
    def __init__(self, label, value):
        super(Gtk.ListBoxRow, self).__init__()
        self.label = label
        self.text = Gtk.Label(label)
        self.add(self.text)
        self.value = value
