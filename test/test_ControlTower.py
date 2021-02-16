import unittest

from ControlTower import ControlTower


class ControlTowerTest(unittest.TestCase):

    def test_predict_threat_should_return_threat_position_range(self):
        tower_info_1 = {"timestamp": "2021-02-12 20:00:20.877533", "lat": 40.41271, "lon": -86.9508, "range": 50, "intensity": "0.05599017", "status": "music"}
        tower_info_2 = {"timestamp": "2021-02-12 20:00:20.877533", "lat": 40.41301, "lon": -86.94991, "range": 50, "intensity": "0.014959198", "status": "music"}
        controlTower = ControlTower()
        controlTower.tower_list["wt1"] = tower_info_1
        controlTower.tower_list["wt2"] = tower_info_2
        result = controlTower.predict_threat()
        self.assertEqual(2, len(controlTower.tower_list))
        self.assertEqual(result['lat'], 40.41277325298627)
        self.assertEqual(result['lon'], -86.95061234947407)

