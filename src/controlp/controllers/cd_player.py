

class CDPlayerController:

    def __init__(self, app, external_model):
        self.app = app
        self.model = external_model

    def back_screen(self):
        self.app.back_screen()

    def load(self):
        self.model.set_active(self.app.config.getboolean('pioneer', 'cd_player'))

    def set_active(self, active: bool):
        if self.model.get_active() != active:
            self.app.config.set('pioneer', 'cd_player', active)
            self.app.config.write()
            self.model.set_active(active)

    def start_stop_cd_player(self):
        """
        Not implemented because I don't have device to investigate protocol and test it
        """
        pass

    def previous(self):
        """
        Not implemented because I don't have device to investigate protocol and test it
        """
        pass

    def play(self):
        """
        Not implemented because I don't have device to investigate protocol and test it
        """
        pass

    def next(self):
        """
        Not implemented because I don't have device to investigate protocol and test it
        """
        pass

    def stop(self):
        """
        Not implemented because I don't have device to investigate protocol and test it
        """
        pass

    def pause(self):
        """
        Not implemented because I don't have device to investigate protocol and test it
        """
        pass
