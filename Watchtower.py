from uuid import uuid4


class Watchtower(object):
    def __init__(self, position, range):
        self.uuid = str(uuid4()).replace('-', '')
        self.position = position
        self.range = range
