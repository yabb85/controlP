from gi.repository import Gio, GObject, Gtk  # type: ignore


class SourceModel(GObject.GObject):
    """
    Model to represente the a source displayed on source widget
    """

    name = GObject.Property(type=str)
    val = GObject.Property()

    def __init__(self, name, val):
        super().__init__()

        self.props.name = name
        self.props.val = val


class CoreSource(Gio.ListStore):
    """
    Model for list of Source
    """

    sources = GObject.Property({})

    def __init__(self, data):
        super().__init__()
        self.sources = dict()
        for key, value in data.items():
            row = SourceModel(*value)
            self.sources[key] = row
            self.append(row)
