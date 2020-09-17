from uuid import uuid4


class Target(object):
    def __init__(self, position):
        self.uuid = str(uuid4()).replace('-', '')
        self.position = position
