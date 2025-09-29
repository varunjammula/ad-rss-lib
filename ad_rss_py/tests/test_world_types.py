import unittest
from ad_rss_py.world.types import (
    RoadSegment,
    RoadSegmentType,
    LaneSegment,
    LaneDrivingDirection,
    LaneSegmentId,
    LateralRssAccelerationValues,
    LongitudinalRssAccelerationValues,
    OccupiedRegion,
)
from ad_rss_py.physics.types import MetricRange, Distance, Acceleration, ParametricRange


class TestWorldTypes(unittest.TestCase):

    def test_road_segment_instantiation(self):
        """
        Test that the RoadSegment dataclass can be instantiated.
        """
        lane_segment = LaneSegment(
            id=LaneSegmentId(1),
            driving_direction=LaneDrivingDirection.Positive,
            length=MetricRange(minimum=0.0, maximum=100.0),
            width=MetricRange(minimum=0.0, maximum=3.5)
        )
        road_segment = RoadSegment(
            type=RoadSegmentType.Normal,
            lane_segments=[lane_segment],
            minimum_length_after_intersecting_area=Distance(10.0),
            minimum_length_before_intersecting_area=Distance(5.0)
        )
        self.assertIsInstance(road_segment, RoadSegment)
        self.assertEqual(road_segment.type, RoadSegmentType.Normal)

    def test_lane_segment_instantiation(self):
        """
        Test that the LaneSegment dataclass can be instantiated.
        """
        lane_segment = LaneSegment(
            id=LaneSegmentId(2),
            driving_direction=LaneDrivingDirection.Bidirectional,
            length=MetricRange(minimum=0.0, maximum=200.0),
            width=MetricRange(minimum=0.0, maximum=4.0)
        )
        self.assertIsInstance(lane_segment, LaneSegment)
        self.assertEqual(lane_segment.id, 2)

    def test_acceleration_values_instantiation(self):
        """
        Test that the acceleration value dataclasses can be instantiated.
        """
        lat_accel = LateralRssAccelerationValues(
            accel_max=Acceleration(2.0),
            brake_min=Acceleration(4.0)
        )
        lon_accel = LongitudinalRssAccelerationValues(
            accel_max=Acceleration(3.0),
            brake_max=Acceleration(8.0),
            brake_min=Acceleration(5.0),
            brake_min_correct=Acceleration(4.0)
        )
        self.assertIsInstance(lat_accel, LateralRssAccelerationValues)
        self.assertIsInstance(lon_accel, LongitudinalRssAccelerationValues)
        self.assertEqual(lat_accel.accel_max, 2.0)
        self.assertEqual(lon_accel.brake_max, 8.0)

    def test_occupied_region_instantiation(self):
        """
        Test that the OccupiedRegion dataclass can be instantiated.
        """
        occupied_region = OccupiedRegion(
            segment_id=LaneSegmentId(3),
            lon_range=ParametricRange(minimum=0.1, maximum=0.2),
            lat_range=ParametricRange(minimum=0.4, maximum=0.6)
        )
        self.assertIsInstance(occupied_region, OccupiedRegion)
        self.assertEqual(occupied_region.segment_id, 3)


if __name__ == '__main__':
    unittest.main()