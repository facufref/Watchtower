from uuid import uuid4


# This class is only for simulation purposes
class Drone(object):
    def __init__(self, position, sound):
        self.uuid = str(uuid4()).replace('-', '')
        self.position = position
        self.sound = sound
