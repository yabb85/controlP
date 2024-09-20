from ..views import InputView

class InputController:

    def __init__(self, app, input_model):
        self.app = app
        self.input_model = input_model

    def choose_input(self, code: int):
        if self.input_model.power_status == 'PWR0':
            if code != self.input_model.input_status:
                self.app.network_player.set_input(code)
                self.input_model.set_input_status(code)
            self.app.set_screen('explore')
