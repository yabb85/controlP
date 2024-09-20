

class AmplifierController:

    def __init__(self, app, amplifier_model):
        self.app = app
        self.amplifier_model = amplifier_model

    def back_screen(self):
        self.app.back_screen()

    def load(self):
        self.amplifier_model.set_active(self.app.config.getboolean('pioneer', 'amplifier'))

    def set_active(self, active: bool):
        if self.amplifier_model.get_active() != active:
            self.app.config.set('pioneer', 'amplifier', active)
            self.app.config.write()
            self.amplifier_model.set_active(active)

    def start_stop_amplifier(self):
        self.app.network_player.ampli_power()

    def change_input(self):
        self.app.network_player.next_source()

    def vol_down(self):
        self.app.network_player.volume_down()

    def vol_up(self):
        self.app.network_player.volume_up()

    def open_window(self):
        self.app.set_previous(self.app.sm.current)
        self.app.set_screen('other_devices')
