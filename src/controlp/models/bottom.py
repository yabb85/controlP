

class BottomModel:
    observers: list = []
    screen: str = ''

    def get_screen(self) -> str:
        return self.screen

    def set_screen(self, screen_name: str):
        self.screen = screen_name
        self.notify_observers()

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.model_is_changed()
