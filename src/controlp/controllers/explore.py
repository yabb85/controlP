from time import sleep
from kivy.clock import Clock


class ExploreController:
    list_size = 50
    cpt = 0

    def __init__(self, app, explore_model, play_model):
        self.app = app
        self.explore_model = explore_model
        self.play_model = play_model
        self.event = None

    def refresh_menu(self):
        """
        Refresh all information needed to display menu
        Check also display of small view completly only display only end lines
        """
        status = self.app.network_player.screen_status()
        if not status:
            self.stop_clock()
            return
        view_type = status.get('type', None)
        if view_type and view_type == '01':
            if status['total_line'] < self.list_size and status['begin_disp'] > 1:
                self.app.network_player.select_line(1)
                status = self.app.network_player.screen_status()
            limit = min(self.list_size, status['total_line'] - status['begin_disp'] + 1)
            new_lines = self.app.network_player.directory_status(
                status['begin_disp'], limit
            )
            status['lines'].update(new_lines)
            status['end_disp'] = status['begin_disp'] + len(new_lines) - 1
            self.explore_model.load(status)
        elif view_type and (view_type == '02' or view_type == '03'):
            img_url = self.app.network_player.img_status()
            status.update(img_url)
            self.play_model.load(status)
            self.app.set_screen('play')
        elif view_type and view_type == '06':
            sleep(0.1)
            self.refresh_menu()

    def explore_set(self, index: int):
        self.app.network_player.set_line(index)
        self.refresh_menu()

    def explore_down(self):
        self.explore_model.scroll_reset = True
        value = min(self.explore_model.last_line + 1, self.explore_model.total_line)
        self.app.network_player.select_line(value)
        self.start_clock()
        self.refresh_menu()

    def explore_up(self):
        # self.explore_model.scroll_reset = True
        value = max(self.explore_model.first_line - self.list_size, 1)
        self.app.network_player.select_line(value)
        self.start_clock()
        self.refresh_menu()

    def explore_return(self):
        self.app.network_player.ret()
        self.refresh_menu()

    def start_clock(self):
        self.event = Clock.schedule_interval(self.clock_refresh_menu, 3)
        self.cpt = 0
        # Clock.schedule_once(self.clock_refresh_menu, 3)

    def stop_clock(self):
        Clock.unschedule(self.event)
        self.cpt = 0

    def clock_refresh_menu(self, dt):
        if self.cpt > 3:
            self.stop_clock()
        self.explore_model.scroll_reset = False
        self.refresh_menu()
        self.cpt += 1

    def back_screen(self):
        self.app.back_screen()
