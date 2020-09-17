from uuid import uuid4


class TowerControl(object):
    def __init__(self):
        self.uuid = str(uuid4()).replace('-', '')

