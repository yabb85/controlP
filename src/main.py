"""
File created specificly to android version
"""

from kivy.factory import Factory
from kivy.graphics import InstructionGroup
from controlp.app import ControlPApp


class NoShadow(InstructionGroup):
    """Stand-in for BoxShadow: accepts its kv properties, draws nothing, makes no Fbo."""

    def __init__(self, **kwargs):
        super().__init__()
        self.pos = (0, 0)
        self.size = (0, 0)
        self.offset = (0, 0)
        self.spread_radius = (0, 0)
        self.blur_radius = 0
        self.border_radius = (0, 0, 0, 0)
        self.inset = False
        for key, value in kwargs.items():
            setattr(self, key, value)


def disable_shadows() -> None:
    # The <CommonElevationBehavior> kv rule (kivymd/uix/behaviors/elevation.py) names `BoxShadow`
    # in canvas.before; kv resolves canvas instruction names via Factory.get() at each widget's
    # build, so swapping the Factory entry covers every elevated widget built afterwards,
    # including the ones KivyMD builds internally.
    Factory.unregister('BoxShadow')
    Factory.register('BoxShadow', cls=NoShadow)


if __name__ == '__main__':
    disable_shadows()
    ControlPApp().run()
