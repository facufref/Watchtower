import json
import pickle
import numpy as np
import logging
import datetime
from datetime import datetime
from uuid import uuid4
from pykafka import KafkaClient
from config import *

client = KafkaClient(hosts='localhost:9092')
topic = client.topics[kafka_topic_name]


class ControlTower(object):
    def __init__(self):
        self.uuid = str(uuid4()).replace('-', '')
        self.tower_list = {}
        self.threat = None
        self.clf = None
        self.producer = topic.get_sync_producer()
        self.last_noise_intensities = []

        with open(clf_model_path, 'rb') as f:
            self.clf = pickle.load(f)

        self.initialize_logging()

    @staticmethod
    def initialize_logging():
        if logging_enabled:
            logging.basicConfig(filename=f'logs/ct-logs-{str(datetime.utcnow()).replace(":", "-")}.log', level=logging.CRITICAL)
            logging.critical(f'classifier = {clf_model_path}')
            logging.critical(f'threat_value = {threat_value}')
            logging.critical(f'recording_time = {recording_time}')
            logging.critical(f'number_of_saved_noises = {number_of_saved_noises}')

    def check_recording(self, tower_id, timestamp, lat, lon, ran, intensity, recording):
        prediction = self.clf.get_predictions(recording)
        self.save_new_noise(intensity, prediction)
        self.tower_list[tower_id] = {
            'timestamp': timestamp,
            'lat': float(lat),
            'lon': float(lon),
            'range': float(ran),
            'intensity': float(intensity),
            'status': prediction[0],
            'isThreatDetected': prediction[0] == threat_value
        }

    def save_new_noise(self, intensity, prediction):
        if prediction[0] != threat_value:
            self.last_noise_intensities.append(float(intensity))
        if len(self.last_noise_intensities) > number_of_saved_noises:
            self.last_noise_intensities.pop(0)

    def check_for_threats(self):
        tower_a_id, tower_b_id = self.get_top_two_towers()
        if tower_a_id is None:
            self.threat = None
        elif tower_b_id is None:
            self.threat = {
                "lat": self.tower_list[tower_a_id]["lat"],
                "lon": self.tower_list[tower_a_id]["lon"],
                "range": self.tower_list[tower_a_id]["range"]
            }
            if logging_enabled:
                logging.critical(f'[{datetime.utcnow()}] Tower {tower_a_id} spotted a threat. Coordinates [{self.tower_list[tower_a_id]["lat"]}; {self.tower_list[tower_a_id]["lon"]}]')
        else:
            predicted_lat, predicted_lon = self.calculate_threat_position(tower_a_id, tower_b_id)
            self.threat = {
                "lat": predicted_lat,
                "lon": predicted_lon,
                "range": self.tower_list[tower_a_id]["range"] * 0.5  # Use 50% of the tower range for now
            }
            if logging_enabled:
                logging.critical(f'[{datetime.utcnow()}] Towers {tower_a_id} and {tower_b_id} spotted a threat. Coordinates [{predicted_lat}; {predicted_lon}]')

    def calculate_threat_position(self, tower_a_id, tower_b_id):
        lat_a = self.tower_list[tower_a_id]["lat"]
        lon_a = self.tower_list[tower_a_id]["lon"]
        lat_b = self.tower_list[tower_b_id]["lat"]
        lon_b = self.tower_list[tower_b_id]["lon"]
        intensity_a = self.tower_list[tower_a_id]["intensity"]
        intensity_b = self.tower_list[tower_b_id]["intensity"]

        np_noise = np.array(self.last_noise_intensities)
        avg_noise = np.average(np_noise)
        stdev_noise = np_noise.std()
        dev_a = intensity_a - avg_noise
        dev_b = intensity_b - avg_noise
        stdev_a = dev_a / stdev_noise
        stdev_b = dev_b / stdev_noise

        ratio = (stdev_b / stdev_a)
        proportion = ratio / (ratio + 1)
        proportion = 1 if proportion > 1 else proportion
        proportion = 0 if proportion < 0 else proportion

        predicted_lat = lat_a + ((lat_b - lat_a) * proportion)
        predicted_lon = lon_a + ((lon_b - lon_a) * proportion)
        return predicted_lat, predicted_lon

    def get_top_two_towers(self):
        first_tower_id = None
        second_tower_id = None

        for tower_id in self.tower_list:
            if not self.tower_list[tower_id]["isThreatDetected"]:
                continue

            if first_tower_id is None:
                first_tower_id = tower_id
            elif self.tower_list[tower_id]["intensity"] >= self.tower_list[first_tower_id]["intensity"]:
                second_tower_id = first_tower_id
                first_tower_id = tower_id
            elif second_tower_id is None or self.tower_list[tower_id]["intensity"] >= self.tower_list[second_tower_id]["intensity"]:
                second_tower_id = tower_id

        return first_tower_id, second_tower_id

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
