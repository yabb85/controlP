

class AmplifierModel:
    observers: list = []
    amplifier: bool = False

    def get_active(self) -> bool:
        return self.active

    def set_active(self, state: bool):
        self.active = state
        self.notify_observers()

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.model_is_changed()
