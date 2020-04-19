from gi.repository import GObject, Gtk  # type: ignore

from ..coremenu import MenuModel


class ListBoxRowSource(Gtk.ListBoxRow):
    def __init__(self, label: str, value: int):
        super(Gtk.ListBoxRow, self).__init__()
        self.label = label
        self.text = Gtk.Label(label)
        self.add(self.text)
        self.value = value


class ListBoxRowEmpty(Gtk.ListBoxRow):
    value = GObject.Property(type=int)

    def __init__(self, menu_model: MenuModel):
        super(Gtk.ListBoxRow, self).__init__()
        self.menu_model = menu_model
        self.value = self.menu_model.props.line_idx
        self.bind_property(
            'value',
            self.menu_model,
            'line_idx',
            GObject.BindingFlags.BIDIRECTIONAL,
        )


class ListBoxRowPicture(Gtk.ListBoxRow):
    def __init__(self, menu_model: MenuModel):
        super(Gtk.ListBoxRow, self).__init__()
        self.box = Gtk.Box(Gtk.Orientation.HORIZONTAL)
        if menu_model.props.pixbuf:
            self.img = Gtk.Image()
            self.img.set_from_pixbuf(menu_model.props.pixbuf)
            self.box.add(self.img)
        self.label = menu_model.props.text
        self.text = Gtk.Label(self.label)
        self.box.add(self.text)
        self.add(self.box)
        self.value = menu_model.props.line_idx
