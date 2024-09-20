from .utils import DeviceDescription


class TopModel:
    observers: list = []
    device: DeviceDescription|None = None
    power_status: bool = False
    screen_type: str|None = None
    image_status: str|None = None
    lines: list = []

    def load(self, device, power_status):
        self.device = device
        self.power_status = power_status
        self.notify_observers()

    def set_device(self, device: DeviceDescription):
        self.device = device
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
