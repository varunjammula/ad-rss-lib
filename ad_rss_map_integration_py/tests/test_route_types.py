import unittest
from ad_rss_map_integration_py.map.route.types import (
    LaneInterval,
    LaneSegment,
    RoadSegment,
    FullRoute,
    RouteCreationMode,
    RouteLaneOffset,
    SegmentCounter,
    RoadSegmentList,
)
from ad_rss_map_integration_py.map.lane.types import LaneId, LaneIdList
from ad_rss_map_integration_py.map.point.types import BoundingSphere, ECEFPoint
from ad_rss_py.physics.types import ParametricValue, Distance


class TestRouteTypes(unittest.TestCase):

    def setUp(self):
        """Set up common mock objects for the tests."""
        self.lane_interval = LaneInterval(
            lane_id=LaneId(1),
            start=ParametricValue(0.0),
            end=ParametricValue(1.0)
        )
        self.lane_segment = LaneSegment(
            left_neighbor=LaneId(0),
            right_neighbor=LaneId(2),
            predecessors=[LaneId(10)],
            successors=[LaneId(20)],
            lane_interval=self.lane_interval,
            route_lane_offset=RouteLaneOffset(0)
        )
        self.bounding_sphere = BoundingSphere(
            center=ECEFPoint(x=0.0, y=0.0, z=0.0),
            radius=Distance(100.0)
        )
        self.road_segment = RoadSegment(
            drivable_lane_segments=[self.lane_segment],
            segment_count_from_destination=SegmentCounter(1),
            bounding_sphere=self.bounding_sphere
        )

    def test_lane_interval_instantiation(self):
        """Test instantiation of the LaneInterval dataclass."""
        self.assertIsInstance(self.lane_interval, LaneInterval)
        self.assertEqual(self.lane_interval.lane_id, 1)

    def test_lane_segment_instantiation(self):
        """Test instantiation of the LaneSegment dataclass."""
        self.assertIsInstance(self.lane_segment, LaneSegment)
        self.assertEqual(self.lane_segment.right_neighbor, 2)

    def test_road_segment_instantiation(self):
        """Test instantiation of the RoadSegment dataclass."""
        self.assertIsInstance(self.road_segment, RoadSegment)
        self.assertEqual(len(self.road_segment.drivable_lane_segments), 1)

    def test_full_route_instantiation(self):
        """Test instantiation of the FullRoute dataclass."""
        full_route = FullRoute(
            road_segments=[self.road_segment],
            route_creation_mode=RouteCreationMode.SameDrivingDirection
        )
        self.assertIsInstance(full_route, FullRoute)
        self.assertEqual(full_route.route_creation_mode, RouteCreationMode.SameDrivingDirection)
        self.assertEqual(len(full_route.road_segments), 1)

if __name__ == '__main__':
    unittest.main()