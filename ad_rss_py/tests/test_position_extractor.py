import unittest
from ad_rss_py.structured.position_extractor import RssObjectPositionExtractor
from ad_rss_py.world.types import (
    OccupiedRegion,
    RoadSegment,
    RoadSegmentType,
    LaneSegment,
    LaneDrivingDirection,
    LaneSegmentId,
)
from ad_rss_py.physics.types import MetricRange, ParametricRange, Distance


class TestRssObjectPositionExtractor(unittest.TestCase):

    def test_position_extraction_logic(self):
        """
        Test the core logic of the RssObjectPositionExtractor.
        """
        # 1. Define occupied regions for a hypothetical object
        # This object occupies the first half of lane 1
        occupied_regions = [
            OccupiedRegion(
                segment_id=LaneSegmentId(1),
                lon_range=ParametricRange(minimum=0.0, maximum=0.5),
                lat_range=ParametricRange(minimum=0.0, maximum=1.0)
            )
        ]

        # 2. Instantiate the extractor
        extractor = RssObjectPositionExtractor(occupied_regions)

        # 3. Feed road and lane segments
        road_segment = RoadSegment(
            type=RoadSegmentType.Normal,
            lane_segments=[], # The extractor doesn't use this directly
            minimum_length_after_intersecting_area=Distance(0.0),
            minimum_length_before_intersecting_area=Distance(0.0)
        )
        extractor.new_road_segment(
            longitudinal_start=MetricRange(minimum=10.0, maximum=10.0),
            road_segment=road_segment
        )

        lane_segment = LaneSegment(
            id=LaneSegmentId(1),
            driving_direction=LaneDrivingDirection.Positive,
            length=MetricRange(minimum=100.0, maximum=100.0), # A 100m long lane
            width=MetricRange(minimum=3.0, maximum=3.0) # A 3m wide lane
        )
        extractor.new_lane_segment(
            lateral_distance=MetricRange(minimum=0.0, maximum=0.0), # First lane
            lane_segment=lane_segment
        )

        # 4. Get the result and assert correctness
        is_complete, dimensions = extractor.get_object_dimensions()

        self.assertTrue(is_complete)

        # Expected longitudinal position: 10m (road_start) + 100m (lane_len) * [0.0, 0.5] = [10, 60]
        self.assertAlmostEqual(dimensions.longitudinal_dimensions.minimum, 10.0)
        self.assertAlmostEqual(dimensions.longitudinal_dimensions.maximum, 60.0)

        # Expected lateral position: 0m (lane_start) + 3m (lane_width) * [0.0, 1.0] = [0, 3]
        self.assertAlmostEqual(dimensions.lateral_dimensions.minimum, 0.0)
        self.assertAlmostEqual(dimensions.lateral_dimensions.maximum, 3.0)

        self.assertTrue(dimensions.on_positive_lane)
        self.assertFalse(dimensions.on_negative_lane)


if __name__ == '__main__':
    unittest.main()