import json
import pickle
from datetime import datetime
from uuid import uuid4

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

    def check_recording(self, tower_id, timestamp, lat, lon, ran, intensity, recording):
        prediction = self.clf.get_predictions(recording)
        self.tower_list[tower_id] = {
            'timestamp': timestamp,
            'lat': lat,
            'lon': lon,
            'range': ran,
            'intensity': intensity,
            'status': prediction[0]
        }

    def predict_threat(self):
        towerA_id = "wt1"
        towerB_id = "wt2"
        latA = self.tower_list[towerA_id]["lat"]
        latB = self.tower_list[towerB_id]["lat"]
        lonA = self.tower_list[towerA_id]["lon"]
        lonB = self.tower_list[towerB_id]["lon"]
        intensityA = self.tower_list[towerA_id]["intensity"]
        intensityB = self.tower_list[towerB_id]["intensity"]
        ratio = (intensityB / intensityA)
        proportion = ratio / (ratio + 1)

        predicted_lat = latA + ((latB - latA) * proportion)
        predicted_lon = lonA + ((lonB - lonA) * proportion)
        return {"lat": predicted_lat, "lon": predicted_lon}

    def delete_old_towers(self):
        obsolete_towers = []
        now = datetime.utcnow()
        for tower_id in self.tower_list:
            timestamp = datetime.strptime(self.tower_list[tower_id]['timestamp'], "%Y-%m-%d %H:%M:%S.%f")
            elapsed = now - timestamp
            if elapsed.total_seconds() > 30:
                obsolete_towers.append(tower_id)

        for tower_id in obsolete_towers:
            del self.tower_list[tower_id]

    def produce_checkpoint(self):
        message = json.dumps(self.tower_list)
        print(message)
        self.producer.produce(message.encode('ascii'))
