import json
import pickle
import time

import numpy as np
import logging
import datetime
from datetime import datetime
from uuid import uuid4
from pykafka import KafkaClient
from config import *
from collections import Counter

client = KafkaClient(hosts='localhost:9092')
topic = client.topics[kafka_topic_name]
elapsed_list = []


class ControlTower(object):
    def __init__(self):
        self.uuid = str(uuid4()).replace('-', '')
        self.tower_dict = {}
        self.threat = None
        self.clf = None
        self.producer = topic.get_sync_producer()

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
            #  Set Flask logger only to Error
            log = logging.getLogger('werkzeug')
            log.setLevel(logging.ERROR)

    def check_recording(self, tower_id, timestamp, lat, lon, ran, intensity, recording):
        # TODO: Remove elapsed time in the future since it may cause additional delays
        start = time.time()
        predictions = self.clf.get_predictions(recording)
        prediction = get_most_frequent_value(predictions)
        end = time.time()
        elapsed = end - start
        elapsed_list.append(elapsed)
        print(f'Prediction time { elapsed }')
        print(f'Average prediction time is { np.mean(elapsed_list) } for { len(elapsed_list) } samples')

        is_tower_registered = tower_id in self.tower_dict.keys()
        self.tower_dict[tower_id] = {
            'timestamp': timestamp,
            'lat': float(lat),
            'lon': float(lon),
            'range': float(ran),
            'intensity': float(intensity),
            'status': prediction,
            'isThreatDetected': prediction == threat_value,
            'lastNoises': self.tower_dict[tower_id]['lastNoises'] if is_tower_registered else []
        }
        self.save_new_noise(tower_id, float(intensity), prediction)
        if log_dev_enabled:
            dev = self.get_deviation(tower_id)
            print(f"Intensity = {intensity} ; Deviation = {dev}")

    def save_new_noise(self, tower_id, intensity, prediction):
        last_noise_intensities = self.tower_dict[tower_id]['lastNoises']
        if prediction != threat_value:
            last_noise_intensities.append(intensity)
        if len(last_noise_intensities) > number_of_saved_noises:
            last_noise_intensities.pop(0)

    def log_threat_position(self):
        tower_a_id, tower_b_id = self.get_top_two_towers()
        if tower_a_id is None:
            self.threat = None
        elif tower_b_id is None:
            self.threat = {
                "lat": self.tower_dict[tower_a_id]["lat"],
                "lon": self.tower_dict[tower_a_id]["lon"],
                "range": self.tower_dict[tower_a_id]["range"]
            }
            if logging_enabled:
                logging.critical(f'[{datetime.utcnow()}] Tower {tower_a_id} spotted a threat. Coordinates [{self.tower_dict[tower_a_id]["lat"]}; {self.tower_dict[tower_a_id]["lon"]}]')
        else:
            predicted_lat, predicted_lon = self.calculate_threat_position(tower_a_id, tower_b_id)
            self.threat = {
                "lat": predicted_lat,
                "lon": predicted_lon,
                "range": self.tower_dict[tower_a_id]["range"] * 0.75  # Use 75% of the tower range for now
            }
            if logging_enabled:
                now = datetime.utcnow()
                logging.critical(f'[{now}] Towers {tower_a_id} and {tower_b_id} spotted a threat. Coordinates [{predicted_lat}; {predicted_lon}]')
                logging.critical(f'[{now}] Tower {tower_a_id} dev = {self.tower_dict[tower_a_id]["dev"]} ; Tower {tower_b_id} dev = {self.tower_dict[tower_b_id]["dev"]} ')

    def calculate_threat_position(self, tower_a_id, tower_b_id):
        lat_a = self.tower_dict[tower_a_id]["lat"]
        lon_a = self.tower_dict[tower_a_id]["lon"]
        lat_b = self.tower_dict[tower_b_id]["lat"]
        lon_b = self.tower_dict[tower_b_id]["lon"]
        dev_a = self.tower_dict[tower_a_id]["dev"]
        dev_b = self.tower_dict[tower_b_id]["dev"]

        ratio = (dev_b / dev_a)
        proportion = ratio / (ratio + 1)
        proportion = 1 if proportion > 1 else proportion
        proportion = 0 if proportion < 0 else proportion

        predicted_lat = lat_a + ((lat_b - lat_a) * proportion)
        predicted_lon = lon_a + ((lon_b - lon_a) * proportion)
        return predicted_lat, predicted_lon

    def get_top_two_towers(self):
        first_tower_id = None
        second_tower_id = None

        for tower_id in self.tower_dict:
            if not self.tower_dict[tower_id]["isThreatDetected"]:
                continue

            self.set_dev(tower_id)

            if first_tower_id is None:
                first_tower_id = tower_id
            elif self.tower_dict[tower_id]["dev"] >= self.tower_dict[first_tower_id]["dev"]:
                second_tower_id = first_tower_id
                first_tower_id = tower_id
            elif second_tower_id is None or self.tower_dict[tower_id]["dev"] >= self.tower_dict[second_tower_id]["dev"]:
                second_tower_id = tower_id

        return first_tower_id, second_tower_id

    def set_dev(self, tower_id):
        dev = self.get_deviation(tower_id)
        self.tower_dict[tower_id]["dev"] = np.abs(dev)

    def get_deviation(self, tower_id):
        intensity = self.tower_dict[tower_id]["intensity"]
        np_noise = np.array(self.tower_dict[tower_id]['lastNoises'])
        median_noise = np.median(np_noise) if len(np_noise) > 0 else intensity
        dev = intensity - median_noise
        return dev

    def delete_old_towers(self):
        obsolete_towers = []
        now = datetime.utcnow()
        for tower_id in self.tower_dict:
            timestamp = datetime.strptime(self.tower_dict[tower_id]['timestamp'], "%Y-%m-%d %H:%M:%S.%f")
            elapsed = now - timestamp
            if elapsed.total_seconds() > time_before_delete_towers:
                obsolete_towers.append(tower_id)

        for tower_id in obsolete_towers:
            del self.tower_dict[tower_id]

    def produce_checkpoint(self):
        message = json.dumps({'towers': self.tower_dict, 'threat': self.threat})
        self.producer.produce(message.encode('ascii'))


def get_most_frequent_value(lst):
    data = Counter(lst)
    return max(lst, key=data.get)
