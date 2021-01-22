from uuid import uuid4
import pickle


class ControlTower(object):
    def __init__(self):
        self.uuid = str(uuid4()).replace('-', '')

    def check_recording(self, lat, lon, recording):
        print(f'Prediction for lat={lat} lon={lon}')
        with open('models/snap_gnb_clf.pkl', 'rb') as f:
            clf = pickle.load(f)

        prediction = clf.get_predictions(recording)
        print(f'The prediction is {prediction}')
