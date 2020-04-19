from gi.repository import GObject  # type: ignore


class CorePower(GObject.GObject):
    network_player_active = GObject.Property(type=bool, default=False)
