import json
import pickle
from datetime import datetime
from uuid import uuid4
from pykafka import KafkaClient
from config import time_before_delete_towers, threat_value, kafka_topic_name

client = KafkaClient(hosts='localhost:9092')
topic = client.topics[kafka_topic_name]


class ControlTower(object):
    def __init__(self):
        self.uuid = str(uuid4()).replace('-', '')
        self.tower_list = {}
        self.threat = None
        self.clf = None
        self.producer = topic.get_sync_producer()

        with open('models/music_gnb_clf_0-5sec.pkl', 'rb') as f:
            self.clf = pickle.load(f)

    def check_recording(self, tower_id, timestamp, lat, lon, ran, intensity, recording):
        prediction = self.clf.get_predictions(recording)
        self.tower_list[tower_id] = {
            'timestamp': timestamp,
            'lat': float(lat),
            'lon': float(lon),
            'range': float(ran),
            'intensity': float(intensity),
            'status': prediction[0],
            'isThreatDetected': prediction[0] == threat_value
        }

    def check_for_threats(self):
        towerA_id, towerB_id = self.get_top_two_towers()
        if towerA_id is None:
            self.threat = None
        elif towerB_id is None:
            self.threat = {
                "lat": self.tower_list[towerA_id]["lat"],
                "lon": self.tower_list[towerA_id]["lon"],
                "range": self.tower_list[towerA_id]["range"]
            }
        else:
            predicted_lat, predicted_lon = self.calculate_threat_position(towerA_id, towerB_id)
            self.threat = {
                "lat": predicted_lat,
                "lon": predicted_lon,
                "range": self.tower_list[towerA_id]["range"] * 0.5  # Use 50% of the tower range for now
            }

    def calculate_threat_position(self, towerA_id, towerB_id):
        latA = self.tower_list[towerA_id]["lat"]
        lonA = self.tower_list[towerA_id]["lon"]
        latB = self.tower_list[towerB_id]["lat"]
        lonB = self.tower_list[towerB_id]["lon"]
        intensityA = self.tower_list[towerA_id]["intensity"]
        intensityB = self.tower_list[towerB_id]["intensity"]
        ratio = (intensityB / intensityA)
        proportion = ratio / (ratio + 1)
        predicted_lat = latA + ((latB - latA) * proportion)
        predicted_lon = lonA + ((lonB - lonA) * proportion)
        return predicted_lat, predicted_lon

    def get_top_two_towers(self):
        firstTowerId = None
        secondTowerId = None

        for tower_id in self.tower_list:
            if not self.tower_list[tower_id]["isThreatDetected"]:
                continue

            if firstTowerId is None:
                firstTowerId = tower_id
            elif self.tower_list[tower_id]["intensity"] >= self.tower_list[firstTowerId]["intensity"]:
                secondTowerId = firstTowerId
                firstTowerId = tower_id
            elif secondTowerId is None or self.tower_list[tower_id]["intensity"] >= self.tower_list[secondTowerId]["intensity"]:
                secondTowerId = tower_id

        return firstTowerId, secondTowerId

    def delete_old_towers(self):
        obsolete_towers = []
        now = datetime.utcnow()
        for tower_id in self.tower_list:
            timestamp = datetime.strptime(self.tower_list[tower_id]['timestamp'], "%Y-%m-%d %H:%M:%S.%f")
            elapsed = now - timestamp
            if elapsed.total_seconds() > time_before_delete_towers:
                obsolete_towers.append(tower_id)

        for tower_id in obsolete_towers:
            del self.tower_list[tower_id]

    def produce_checkpoint(self):
        message = json.dumps({'towers': self.tower_list, 'threat': self.threat})
        print(message)
        self.producer.produce(message.encode('ascii'))
