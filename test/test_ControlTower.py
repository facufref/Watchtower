import unittest

from ControlTower import ControlTower
last_noises = [0.010541213, 0.010367212, 0.010551292, 0.010367212, 0.010551292, 0.010547385, 0.010795445, 0.010547385, 0.010795445, 0.010522221]
tower_info_1 = {"timestamp": "2021-02-12 20:00:20.877533", "lat": 40.41271, "lon": -86.9508, "range": 50, "intensity": 0.05599017, "status": "music", "isThreatDetected": True, "lastNoises": last_noises}
tower_info_2 = {"timestamp": "2021-02-12 20:00:20.877533", "lat": 40.41301, "lon": -86.94991, "range": 50, "intensity": 0.050959198, "status": "music", "isThreatDetected": True, "lastNoises": last_noises}
tower_info_3 = {"timestamp": "2021-02-12 20:00:20.877533", "lat": 0.0, "lon": 0.0, "range": 0.0, "intensity": 0.0002, "status": "music", "isThreatDetected": True, "lastNoises": last_noises}
tower_info_4 = {"timestamp": "2021-02-12 20:00:20.877533", "lat": 0.0, "lon": 0.0, "range": 0.0, "intensity": 0.0001, "status": "music", "isThreatDetected": True, "lastNoises": last_noises}


class ControlTowerTest(unittest.TestCase):

    def test_predict_threat_should_return_threat_position_range(self):
        control_tower = ControlTower()
        control_tower.tower_dict["wt1"] = tower_info_1
        control_tower.tower_dict["wt2"] = tower_info_2
        control_tower.log_threat_position()
        self.assertEqual(2, len(control_tower.tower_dict))
        self.assertEqual(control_tower.threat['lat'], 40.41285121018772)
        self.assertEqual(control_tower.threat['lon'], -86.95038107644311)
        self.assertEqual(control_tower.threat['range'], 37.5)

    def test_get_top_two_towers_should_return_top_two(self):
        control_tower = ControlTower()
        control_tower.tower_dict["ignored1"] = tower_info_3
        control_tower.tower_dict["ignored2"] = tower_info_4
        control_tower.tower_dict["wt1"] = tower_info_1
        control_tower.tower_dict["wt2"] = tower_info_2
        first_id, second_id = control_tower.get_top_two_towers()
        self.assertEqual(first_id, 'wt1')
        self.assertEqual(second_id, 'wt2')

    def test_get_top_two_towers_with_false_detection_should_return_top_two(self):
        control_tower = ControlTower()
        control_tower.tower_dict["wt1"] = tower_info_1
        control_tower.tower_dict["wt2"] = tower_info_2
        control_tower.tower_dict["wt3"] = tower_info_3
        control_tower.tower_dict["wt4"] = tower_info_4
        control_tower.tower_dict["wt1"]["isThreatDetected"] = False
        first_id, second_id = control_tower.get_top_two_towers()
        self.assertEqual(first_id, 'wt2')
        self.assertEqual(second_id, 'wt3')
