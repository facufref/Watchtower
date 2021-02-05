from datetime import datetime
from uuid import uuid4
from classifier.SoundDataManager import get_dataset_from_array
from classifier.SoundRecorder import get_recording, write_recording
import requests


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
        recording = get_recording(duration=1)
        timestamp = str(datetime.utcnow())

        if self.save_recording:
            write_recording(recording, f'recordings/recording {timestamp.replace(":", "-")}.wav')

        recording_mfcc_list = get_dataset_from_array(44100, recording, 0.5)
        requests.post(f'http://localhost:5001/check', json={'tower_id': self.tower_id,
                                                            'position_lat': self.position_lat,
                                                            'position_lon': self.position_lon,
                                                            'timestamp': timestamp,
                                                            'range': self.range,
                                                            'recording': recording_mfcc_list.tolist()
                                                            })
        return recording_mfcc_list

    def record_forever(self):
        while True:
            requests.get(f'http://localhost:{self.port}/record')
