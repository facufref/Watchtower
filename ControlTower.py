from uuid import uuid4
import pickle


class ControlTower(object):
    def __init__(self):
        self.uuid = str(uuid4()).replace('-', '')
        self.tower_list = {}
        self.clf = None

        with open('models/music_gnb_clf_0-5sec.pkl', 'rb') as f:
            self.clf = pickle.load(f)

    def check_recording(self, tower_id, lat, lon, recording):
        prediction = self.clf.get_predictions(recording)
        self.tower_list[tower_id] = {
            'lat': lat,
            'lon': lon,
            'status': prediction
        }
        print(self.tower_list)
