from uuid import uuid4


class Target(object):
    def __init__(self, position_lat, position_lon):
        self.uuid = str(uuid4()).replace('-', '')
        self.position_lat = position_lat
        self.position_lon = position_lon
