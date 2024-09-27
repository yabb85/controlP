from time import sleep
from kivy.clock import Clock

class ExploreController:
    list_size = 50
    cpt = 0
    plop = 0

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
        for index, line in status['lines'].items():
            if line['highlight'] == '1':
                self.explore_model.set_selected_line(index + status['begin_disp'] - 1)
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
            self.planify_preload()
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

    def explore_return(self):
        self.app.network_player.ret()
        self.refresh_menu()

    def planify_preload(self):
        """
        Start preload execution if display menu list
        """
        if self.explore_model.get_preload_status():
            Clock.schedule_once(self.preload, 1)

    def preload(self, dt):
        """
        preload data to feed cache and avoid latency in big menu
        """
        first_line = self.explore_model.first_line
        last_line = self.explore_model.last_line
        if first_line != 1:
            limit = max(first_line - self.list_size, first_line - 1)
            begin = first_line - limit
        else:
            begin = last_line + 1
            limit = min(self.list_size, self.explore_model.total_line - last_line)
        if limit != 0:
            new_lines = self.app.network_player.directory_status(
                begin, limit
            )
            self.explore_model.preload_update(new_lines)
        if self.explore_model.get_preload_status():
            self.preload(None)
        else:
            self.explore_model.notify_observers()

    def back_screen(self):
        self.app.back_screen()
