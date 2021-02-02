import json
from datetime import datetime, date
from uuid import uuid4
import pickle
from pykafka import KafkaClient

client = KafkaClient(hosts='localhost:9092')
topic = client.topics['watchtower']


class ControlTower(object):
    def __init__(self):
        self.uuid = str(uuid4()).replace('-', '')
        self.tower_list = {}
        self.clf = None
        self.producer = topic.get_sync_producer()

        with open('models/music_gnb_clf_0-5sec.pkl', 'rb') as f:
            self.clf = pickle.load(f)

    def check_recording(self, tower_id, lat, lon, recording):
        prediction = self.clf.get_predictions(recording)
        self.tower_list[tower_id] = {
            'timestamp': str(datetime.utcnow()),
            'lat': lat,
            'lon': lon,
            'status': prediction[0]
        }

    def delete_old_towers(self):
        obsolete_towers = []
        now = datetime.utcnow()
        for uuid in self.tower_list:
            timestamp = datetime.strptime(self.tower_list[uuid]['timestamp'], "%Y-%m-%d %H:%M:%S.%f")
            elapsed = now - timestamp
            if elapsed.total_seconds() > 30:
                obsolete_towers.append(uuid)

        for uuid in obsolete_towers:
            del self.tower_list[uuid]

    def produce_checkpoint(self):
        message = json.dumps(self.tower_list)
        print(message)
        self.producer.produce(message.encode('ascii'))
