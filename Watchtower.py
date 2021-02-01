from uuid import uuid4
from classifier.SoundDataManager import get_dataset_from_array
from classifier.SoundRecorder import get_recording, write_recording
import requests


class Watchtower(object):
    def __init__(self, lat, lon, ran, port):
        self.uuid = str(uuid4()).replace('-', '')
        self.position_lat = lat
        self.position_lon = lon
        self.range = ran
        self.port = port
        self.count = 1  # TODO: Remove

    def record(self):
        print("Recording...")
        recording = get_recording(duration=0.5)
        # write_recording(recording, f'background{self.count}.wav')  # TODO: Remove
        # self.count += 1  # TODO: Remove
        recording_mfcc_list = get_dataset_from_array(44100, recording, 0.5)
        requests.post(f'http://localhost:5000/check', json={'uuid': self.uuid,
                                                            'position_lat': self.position_lat,
                                                            'position_lon': self.position_lon,
                                                            'recording': recording_mfcc_list.tolist()
                                                            })
        return recording_mfcc_list

    def record_forever(self):
        while True:
            requests.get(f'http://localhost:{self.port}/record')
