

class BottomController:

    def __init__(self, app, bottom_model, explore_controller):
        self.app = app
        self.bottom_model = bottom_model
        self.explore_controller = explore_controller

    def set_screen(self, screen_name=None):
        if not screen_name:
            screen_name = self.app.sm.current
        self.bottom_model.set_screen(screen_name)

    def current_play(self):
        print('current_play')
        self.app.network_player.current_play()
        self.app.set_screen('play')

    def refresh_view(self):
        if self.bottom_model.get_screen() == 'explore':
            self.explore_controller.refresh_menu()
