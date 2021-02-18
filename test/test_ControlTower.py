import unittest

from ControlTower import ControlTower

tower_info_1 = {"timestamp": "2021-02-12 20:00:20.877533", "lat": 40.41271, "lon": -86.9508, "range": 50, "intensity": 0.05599017, "status": "music", "isThreatDetected": True}
tower_info_2 = {"timestamp": "2021-02-12 20:00:20.877533", "lat": 40.41301, "lon": -86.94991, "range": 50, "intensity": 0.014959198, "status": "music", "isThreatDetected": True}
tower_info_3 = {"timestamp": "2021-02-12 20:00:20.877533", "lat": 0.0, "lon": 0.0, "range": 0.0, "intensity": 0.0002, "status": "music", "isThreatDetected": True}
tower_info_4 = {"timestamp": "2021-02-12 20:00:20.877533", "lat": 0.0, "lon": 0.0, "range": 0.0, "intensity": 0.0001, "status": "music", "isThreatDetected": True}


class ControlTowerTest(unittest.TestCase):

    def test_predict_threat_should_return_threat_position_range(self):
        controlTower = ControlTower()
        controlTower.tower_list["wt1"] = tower_info_1
        controlTower.tower_list["wt2"] = tower_info_2
        controlTower.last_noise_intensities = [0.010541213, 0.010367212, 0.010551292, 0.010367212, 0.010551292, 0.010547385, 0.010795445, 0.010547385, 0.010795445, 0.010522221]
        controlTower.check_for_threats()
        self.assertEqual(2, len(controlTower.tower_list))
        self.assertEqual(controlTower.threat['lat'], 40.41273649246327)
        self.assertEqual(controlTower.threat['lon'], -86.95072140569229)
        self.assertEqual(controlTower.threat['range'], 25)

    def test_get_top_two_towers_should_return_top_two(self):
        controlTower = ControlTower()
        controlTower.tower_list["ignored1"] = tower_info_3
        controlTower.tower_list["ignored2"] = tower_info_4
        controlTower.tower_list["wt1"] = tower_info_1
        controlTower.tower_list["wt2"] = tower_info_2
        first_id, second_id = controlTower.get_top_two_towers()
        self.assertEqual(first_id, 'wt1')
        self.assertEqual(second_id, 'wt2')

    def test_get_top_two_towers_with_false_detection_should_return_top_two(self):
        controlTower = ControlTower()
        controlTower.tower_list["wt1"] = tower_info_1
        controlTower.tower_list["wt2"] = tower_info_2
        controlTower.tower_list["wt3"] = tower_info_3
        controlTower.tower_list["wt4"] = tower_info_4
        controlTower.tower_list["wt1"]["isThreatDetected"] = False
        first_id, second_id = controlTower.get_top_two_towers()
        self.assertEqual(first_id, 'wt2')
        self.assertEqual(second_id, 'wt3')
