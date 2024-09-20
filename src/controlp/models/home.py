from .utils import DeviceDescription


class HomeModel:
    observers: list = []
    devices: dict[str, DeviceDescription] = {}

    def refres_all(self, devices):
        """
        Refresh all list of devices available in local network
        """
        for device in devices:
            self.devices[device['friendly_name']] = DeviceDescription(device)
        self.notify_observers()

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.model_is_changed()
