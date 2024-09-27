

class BottomController:

    def __init__(self, app, bottom_model):
        self.app = app
        self.bottom_model = bottom_model

    def set_screen(self, screen_name=None):
        if not screen_name:
            screen_name = self.app.sm.current
        self.bottom_model.set_screen(screen_name)

    def current_play(self):
        self.app.network_player.current_play()
        self.app.set_screen('play')

    def refresh_view(self):
        pass
