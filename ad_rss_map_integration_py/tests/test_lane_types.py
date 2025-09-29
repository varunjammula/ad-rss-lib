import unittest
from ad_rss_map_integration_py.map.lane.types import LaneId, LaneIdList

class TestLaneTypes(unittest.TestCase):

    def test_lane_id_assignment(self):
        """
        Test that LaneId can be assigned and used as an integer.
        """
        lane_id: LaneId = 123
        self.assertEqual(lane_id, 123)
        self.assertIsInstance(lane_id, int)

    def test_lane_id_list_assignment(self):
        """
        Test that LaneIdList can be assigned and used as a list of integers.
        """
        lane_list: LaneIdList = [1, 2, 3]
        self.assertEqual(len(lane_list), 3)
        self.assertIsInstance(lane_list[0], int)

if __name__ == '__main__':
    unittest.main()