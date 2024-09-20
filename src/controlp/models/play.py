from datetime import timedelta

class PlayModel:
    observers: list = []
    title: str|None = None
    artist: str|None = None
    album: str|None = None
    encoding: str|None = None
    sampling: str|None = None
    resolution: str|None = None
    elapsed_time: str|None = None
    elapsed_time_s: timedelta|None = None
    duration: str|None = None
    duration_s: timedelta|None = None
    img_url: str|None = None
    shuffle: int|None = None
    repeat: int|None = None
    play: int = 0

    def load(self, status):
        self.img_url = status.get('url', None)
        self.shuffle = status.get('shuffle', 0)
        self.repeat = status.get('repeat', 0)
        self.play = status.get('play', 0)
        lines = status.get('lines', {})
        self.title = lines.get(1, {}).get('value', '')
        self.artist = lines.get(2, {}).get('value', '')
        self.album = lines.get(3, {}).get('value', '')
        self.encoding = lines.get(4, {}).get('value', '')
        self.sampling = lines.get(5, {}).get('value', '')
        self.resolution = lines.get(6, {}).get('value', '')
        self.elapsed_time = lines.get(7, {}).get('value', '')
        if self.elapsed_time:
            minutes, secondes = self.elapsed_time.split(':')
            self.elapsed_time_s = timedelta(minutes=int(minutes), seconds=int(secondes))
        self.duration = lines.get(8, {}).get('value', None)
        if self.duration:
            minutes, secondes = self.duration.split(':')
            self.duration_s = timedelta(minutes=int(minutes), seconds=int(secondes))
        self.notify_observers()

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.model_is_changed()
