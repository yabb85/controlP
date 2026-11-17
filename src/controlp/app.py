from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.utils import platform
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.navigationdrawer import MDNavigationLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager

from .controllers import InputController, TopController, HomeController, ExploreController, PlayController, AmplifierController, CDPlayerController, BottomController
from .models import TopModel, HomeModel, ExploreModel, PlayModel, InputModel, AmplifierModel, CDPlayerModel, BottomModel
from .views import InputView, HomeView, ExploreView, PlayView, OtherDevicesView
from .pioneer import Pioneer


class ControlPApp(MDApp):
    network_player: Pioneer|None = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.home_model = HomeModel()
        self.top_model = TopModel()
        self.input_model = InputModel()
        self.explore_model = ExploreModel()
        self.play_model = PlayModel()
        self.amplifier_model = AmplifierModel()
        self.cd_player_model = CDPlayerModel()
        self.bottom_model = BottomModel()

        self.home_controller = HomeController(self, self.home_model, self.top_model, self.input_model)
        self.input_controller = InputController(self, self.input_model)
        self.top_controller = TopController(self, self.top_model, self.input_model)
        self.explore_controller = ExploreController(self, self.explore_model, self.play_model)
        self.play_controller = PlayController(self, self.play_model, self.bottom_model)
        self.amplifier_controller = AmplifierController(self, self.amplifier_model)
        self.cd_player_controller = CDPlayerController(self, self.cd_player_model)
        self.bottom_controller = BottomController(self, self.bottom_model, self.explore_controller)

        self.home_view = HomeView(controller=self.home_controller, model=self.home_model)
        self.input_view = InputView(
            top_controller=self.top_controller,
            top_model=self.top_model,
            input_controller=self.input_controller,
            input_model=self.input_model,
            amplifier_controller=self.amplifier_controller,
            amplifier_model=self.amplifier_model,
            bottom_controller=self.bottom_controller,
            bottom_model=self.bottom_model,
        )
        self.explore_view = ExploreView(
            top_controller=self.top_controller,
            top_model=self.top_model,
            explore_controller=self.explore_controller,
            explore_model=self.explore_model,
            amplifier_controller=self.amplifier_controller,
            amplifier_model=self.amplifier_model,
            bottom_controller=self.bottom_controller,
            bottom_model=self.bottom_model,
        )
        self.play_view = PlayView(
            top_controller=self.top_controller,
            top_model=self.top_model,
            play_controller=self.play_controller,
            play_model=self.play_model,
            amplifier_controller=self.amplifier_controller,
            amplifier_model=self.amplifier_model,
            bottom_controller=self.bottom_controller,
            bottom_model=self.bottom_model,
        )
        self.other_devices_view = OtherDevicesView(
            amplifier_controller=self.amplifier_controller,
            amplifier_model=self.amplifier_model,
            cd_player_controller=self.cd_player_controller,
            cd_player_model=self.cd_player_model,
        )
        self.previous_view = None

    def build(self):
        self.theme_cls.theme_style = "Dark"
        # self.theme_cls.primary_palette = "Olive"
        self.theme_cls.primary_palette = "Darkorange"
        # self.theme_cls.dynamic_scheme_name = "FRUIT_SALAD"
        self.theme_cls.dynamic_scheme_name = "RAINBOW"
        self.sm = MDScreenManager()
        self.sm.add_widget(self.home_view)
        self.sm.add_widget(self.input_view)
        self.sm.add_widget(self.explore_view)
        self.sm.add_widget(self.play_view)
        self.sm.add_widget(self.other_devices_view)
        self.sm.current = 'home'
        # return self.sm
        # insets fix: Android 15+ (targetSdk 35+) draws the app under the status / navigation bars.
        # Padding the MDScreenManager does nothing, so the manager sits in a box that gets the padding;
        # the rest of the app keeps using self.sm. Insets are read at the first frame and again 1 s
        # later (the window is fully attached by then).
        self.root_box = MDBoxLayout()
        self.root_box.add_widget(self.sm)
        Clock.schedule_once(lambda dt: self.apply_insets(), 0)
        Clock.schedule_once(lambda dt: self.apply_insets(), 1)
        return self.root_box

    def build_config(self, config):
        config.setdefaults('pioneer',
            {
                'amplifier': False,
                'cd_player': False,
            }
        )

    def back_screen(self):
        self.set_screen(self.previous_view)

    def set_previous(self, previous):
        self.previous_view = previous

    def set_screen(self, view_name: str):
        self.sm.current = view_name
        # self.sm.current = 'list'

    def set_network_player(self, network_player):
        self.network_player = network_player

    def apply_insets(self) -> None:
        # read the system bar insets (px); pad the root box by them when they are readable
        ins = read_insets()
        top, bottom, left, right = ins if ins is not None else ('n/a',) * 4
        applied = ins is not None
        if applied:
            self.root_box.padding = [left, top, right, bottom]  # Kivy padding = left, top, right, bottom


def read_insets():
    """(top, bottom, left, right) insets in px = system bars + display cutout (max per side), or None
    off Android / before attach. Also prints `STUB insets parts bars=t,b,l,r cutout=t,b,l,r`."""
    try:
        from jnius import autoclass
    except Exception:  # noqa: BLE001 - desktop
        return None
    try:
        activity = autoclass('org.kivy.android.PythonActivity').mActivity
        ins = activity.getWindow().getDecorView().getRootWindowInsets()
        if ins is None:
            return None
        sdk = autoclass('android.os.Build$VERSION').SDK_INT
        if sdk >=30:
            types = autoclass('android.view.WindowInsets$Type')
            bars_i = ins.getInsets(types.systemBars())
            cut_i = ins.getInsets(types.displayCutout())
            both = ins.getInsets(types.systemBars() | types.displayCutout())  # Type ints OR together
            bars = (bars_i.top, bars_i.bottom, bars_i.left, bars_i.right)
            cutout = (cut_i.top, cut_i.bottom, cut_i.left, cut_i.right)
            total = (both.top, both.bottom, both.left, both.right)
        else:
            bars = (ins.getSystemWindowInsetTop(), ins.getSystemWindowInsetBottom(),
                    ins.getSystemWindowInsetLeft(), ins.getSystemWindowInsetRight())
            dc = ins.getDisplayCutout() if sdk >= 28 else None  # API 28+; None = no cutout
            cutout = ((dc.getSafeInsetTop(), dc.getSafeInsetBottom(),
                       dc.getSafeInsetLeft(), dc.getSafeInsetRight()) if dc is not None else (0, 0, 0, 0))
            total = tuple(max(a, b) for a, b in zip(bars, cutout))
        print(f'STUB insets parts bars={",".join(map(str, bars))} cutout={",".join(map(str, cutout))}')
        return total
    except Exception as e:  # noqa: BLE001 - diagnostics only
        print('STUB insets error', repr(e))
        return None
