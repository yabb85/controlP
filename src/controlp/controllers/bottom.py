

class BottomController:

    def __init__(self, app, model):
        self.app = app
        self.model = model

    def set_screen(self, screen_name=None):
        if not screen_name:
            screen_name = self.app.sm.current
        self.model.set_screen(screen_name)

    def current_play(self):
        self.app.network_player.current_play()
