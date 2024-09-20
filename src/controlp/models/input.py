

class InputModel:
    observers: list = []
    power_status: bool = False
    input_status: int|None = None
    _sources = {
        13: 'DAC',
        17: 'iPod/USB Front',
        38: 'Internet Radio',
        44: 'Music Server',
        45: 'Favorites',
        57: 'Spotify',
        59: 'Digital Input 1',
        60: 'Digital Input 2',
        61: 'iPod/USB Rear',
    }

    def load(self, input_status, power_status):
        self.input_status = input_status
        self.power_status = power_status
        self.notify_observers()

    def set_input_status(self, input_status):
        self.input_status = input_status
        self.notify_observers()

    def set_power_status(self, power_status):
        self.power_status = power_status
        self.notify_observers()

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.model_is_changed()
