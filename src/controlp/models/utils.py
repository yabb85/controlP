

class DeviceDescription:
    friendly_name: str|None = None
    model: str|None = None
    remote_ready: str|None = None
    remote_port: int = 0
    remote_ip: str|None = None

    def __init__(self, data: dict):
        self.friendly_name = data['friendly_name']
        self.model = data['model']
        self.remote_ready = data['remote_ready']
        self.remote_port = data['remote_port']
        self.remote_ip = data['remote_ip']
