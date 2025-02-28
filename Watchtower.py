from datetime import datetime
from uuid import uuid4
from classifier.SoundDataManager import get_dataset_from_array
from config import control_tower_ip, recording_time, feature_type, chunk_size, is_recording_only
import classifier.SoundRecorder as sr
import requests
import numpy as np


class Watchtower(object):
    def __init__(self, tower_id, lat, lon, port, ran, save_recording):
        self.tower_id = str(uuid4()).replace('-', '') if tower_id is None else tower_id
        self.position_lat = lat
        self.position_lon = lon
        self.port = port
        self.range = ran
        self.save_recording = save_recording

    def record(self):
        print("Recording...")
        recording = sr.get_recording(duration=recording_time)
        timestamp = str(datetime.utcnow())

        if self.save_recording:
            sr.write_recording(recording, f'recordings/recording {timestamp.replace(":", "-")}.wav')
            if is_recording_only:
                return None

        recording_feature_list = get_dataset_from_array(44100, recording, chunk_size, feature_type=feature_type)
        requests.post(f'{control_tower_ip}/check', json={'tower_id': self.tower_id,
                                                            'position_lat': self.position_lat,
                                                            'position_lon': self.position_lon,
                                                            'timestamp': timestamp,
                                                            'range': self.range,
                                                            'intensity': str(sr.get_rms(recording)),
                                                            'recording': recording_feature_list.tolist()
                                                            })
        return recording_feature_list.tolist()

    def record_forever(self):
        while True:
            requests.get(f'http://localhost:{self.port}/record')
