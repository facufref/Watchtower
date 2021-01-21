from uuid import uuid4
import threading

from ..classifier import SoundDataManager as sdm
from SoundRecorder import get_recording


class Watchtower(object):
    def __init__(self):
        self.uuid = str(uuid4()).replace('-', '')
        self.position_lat = None
        self.position_lon = None
        self.range = None

        # The watchtower starts to send the recording to control tower and does it forever
        thread = threading.Thread(target=record_forever(), args=())
        thread.daemon = True
        thread.start()


def record():
    recording = get_recording()
    recording_mfcc_list = sdm.get_dataset_from_array(44100, recording, 3.5)
    print(recording_mfcc_list)


def record_forever():
    while True:
        print("Recording...")
        record()
