from ..pioneer import Pioneer


class TopController:

    def __init__(self, app, top_model, input_model):
        self.app = app
        self.top_model = top_model
        self.input_model = input_model

    def set_previous(self, previous):
        self.app.set_previous(previous)

    def back_screen(self):
        self.app.back_screen()

    def power(self):
        if self.top_model.power_status == 'PWR0':
            self.app.network_player.power_off()
            self.top_model.set_power_status('PWR2')
            self.input_model.set_power_status('PWR2')
            self.app.set_screen('input')
        else:
            self.app.network_player.power_on()
            self.top_model.set_power_status('PWR0')
            self.input_model.set_power_status('PWR0')
        self.app.network_player._clean_buffer()
