from uuid import uuid4


class Watchtower(object):
    def __init__(self):
        self.uuid = str(uuid4()).replace('-', '')
        self.position_lat = None
        self.position_lon = None
        self.range = None
