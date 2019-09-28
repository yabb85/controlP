from gi.repository import GObject


class CorePower(GObject.GObject):
    network_player_active = GObject.Property(type=bool, default=False)
