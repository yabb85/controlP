from kivy.utils import platform
from ..views import HomeView
from ..pioneer import Pioneer, scan

class HomeController:

    def __init__(self, app, home_model, top_model, input_model):
        self.app = app
        self.home_model = home_model
        self.top_model = top_model
        self.input_model = input_model
        # self.view = HomeView(controller=self, model=self.model)
        self.load()

    def back_screen(self):
        # self.app.back_screen()
        return True

    def load(self):
        devices = scan()
        self.home_model.refres_all(devices)

    def choose(self, name: str):
        device = self.home_model.devices[name]
        if not self.top_model.device or (device and self.top_model.device.friendly_name != device.friendly_name):
            if self.app.network_player:
                self.app.network_player.close()
            self.app.set_network_player(Pioneer(device.remote_ip, device.remote_port))
            power_status = self.app.network_player.power_status()
            self.top_model.load(device, power_status)
            input_status = self.app.network_player.input_status()
            self.input_model.load(input_status, power_status)
        elif device and self.top_model.device.friendly_name == device.friendly_name and self.app.network_player:
            input_status = self.app.network_player.input_status()
            if self.input_model.input_status != input_status:
                self.input_model.set_input_status(input_status)
            power_status = self.app.network_player.power_status()
            if self.top_model.power_status != power_status:
                self.top_model.set_power_status(power_status)
                self.input_model.set_power_status(power_status)
        self.app.set_screen('input')
