from datetime import timedelta
from time import sleep

from kivy.clock import Clock


class PlayController:

    def __init__(self, app, play_model):
        self.app = app
        self.play_model = play_model
        self.event = None

    def refresh_status(self):
        status = self.app.network_player.screen_status()
        view_type = status.get('type', None)
        if view_type and view_type == '01':
            self.app.set_screen('explore')
        elif view_type and (view_type == '02' or view_type == '03'):
            img_url = self.app.network_player.img_status()
            status.update(img_url)
            self.play_model.load(status)
        elif view_type and view_type == '06':
            sleep(0.1)
            self.refresh_status()

    def previous(self):
        self.app.network_player.previous()
        self.refresh_status()

    def play_pause(self):
        if self.play_model.play == 0 or self.play_model.play == 1:
            self.app.network_player.play()
        elif self.play_model.play == 2:
            self.app.network_player.pause()
        self.refresh_status()

    def next(self):
        self.app.network_player.next()
        self.refresh_status()

    def shuffle(self):
        self.app.network_player.shuffle()
        self.refresh_status()

    def repeat(self):
        self.app.network_player.repeat()
        self.refresh_status()

    def start_clock(self):
        self.event = Clock.schedule_interval(self.clock_refresh, 1)

    def stop_clock(self):
        Clock.unschedule(self.event)

    def clock_refresh(self, dt):
        diff = timedelta(milliseconds=dt * 1000)
        if self.play_model.play == 2:
            self.play_model.elapsed_time_s += diff
            if self.play_model.elapsed_time_s < self.play_model.duration_s:
                minutes = int(self.play_model.elapsed_time_s / timedelta(minutes=1))
                seconds = self.play_model.elapsed_time_s.seconds % 60
                self.play_model.elapsed_time = f'{minutes}:{seconds:02}'
                self.play_model.notify_observers()
            else:
                self.refresh_status()

    def back_screen(self):
        self.app.network_player.ret()
        self.app.back_screen()
