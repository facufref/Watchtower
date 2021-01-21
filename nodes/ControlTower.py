from uuid import uuid4


class ControlTower(object):
    def __init__(self):
        self.uuid = str(uuid4()).replace('-', '')

