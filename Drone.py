from uuid import uuid4


# This class is only for simulation purposes
class Drone(object):
    def __init__(self, position_lat, position_lon, sound):
        self.uuid = str(uuid4()).replace('-', '')
        self.position_lat = position_lat
        self.position_lon = position_lon
        self.sound = sound
