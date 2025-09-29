import unittest
from ad_rss_map_integration_py.map.match.types import (
    LanePoint,
    MapMatchedPosition,
    MapMatchedPositionType,
    LaneOccupiedRegion,
    MapMatchedObjectBoundingBox,
    ENUObjectPosition,
    Object as MapMatchedObject,
    Probability,
)
from ad_rss_map_integration_py.map.point.types import (
    ParaPoint,
    ENUPoint,
    ECEFPoint,
    GeoPoint,
    ENUHeading,
)
from ad_rss_map_integration_py.map.lane.types import LaneId
from ad_rss_py.physics.types import Distance, RatioValue, Dimension3D, ParametricRange


class TestMatchTypes(unittest.TestCase):

    def setUp(self):
        """Set up common mock objects for the tests."""
        self.para_point = ParaPoint(lane_id=LaneId(1), parametric_offset=0.5)
        self.enu_point = ENUPoint(x=1.0, y=2.0, z=3.0)
        self.geo_point = GeoPoint(longitude=8.0, latitude=49.0, altitude=100.0)
        self.dimension = Dimension3D(length=4.0, width=1.8, height=1.5)

    def test_lane_point_instantiation(self):
        """Test instantiation of the LanePoint dataclass."""
        lane_point = LanePoint(
            para_point=self.para_point,
            lateral_t=RatioValue(0.5),
            lane_length=Distance(100.0),
            lane_width=Distance(3.5)
        )
        self.assertIsInstance(lane_point, LanePoint)
        self.assertEqual(lane_point.para_point.lane_id, 1)

    def test_map_matched_position_instantiation(self):
        """Test instantiation of the MapMatchedPosition dataclass."""
        lane_point = LanePoint(self.para_point, 0.5, 100.0, 3.5)
        ecef_point = ECEFPoint(x=0, y=0, z=0)

        pos = MapMatchedPosition(
            lane_point=lane_point,
            type=MapMatchedPositionType.LANE_IN,
            matched_point=ecef_point,
            query_point=ecef_point,
            probability=Probability(0.9),
            matched_point_distance=Distance(0.1)
        )
        self.assertIsInstance(pos, MapMatchedPosition)
        self.assertEqual(pos.type, MapMatchedPositionType.LANE_IN)

    def test_lane_occupied_region_instantiation(self):
        """Test instantiation of the LaneOccupiedRegion dataclass."""
        region = LaneOccupiedRegion(
            lane_id=LaneId(1),
            longitudinal_range=ParametricRange(minimum=0.2, maximum=0.4),
            lateral_range=ParametricRange(minimum=-0.5, maximum=0.5)
        )
        self.assertIsInstance(region, LaneOccupiedRegion)
        self.assertEqual(region.lane_id, 1)

    def test_map_matched_object_bounding_box_instantiation(self):
        """Test instantiation of the MapMatchedObjectBoundingBox dataclass."""
        bbox = MapMatchedObjectBoundingBox()
        self.assertIsInstance(bbox, MapMatchedObjectBoundingBox)
        self.assertEqual(len(bbox.lane_occupied_regions), 0)

    def test_enu_object_position_instantiation(self):
        """Test instantiation of the ENUObjectPosition dataclass."""
        pos = ENUObjectPosition(
            center_point=self.enu_point,
            heading=ENUHeading(1.57),
            enu_reference_point=self.geo_point,
            dimension=self.dimension
        )
        self.assertIsInstance(pos, ENUObjectPosition)
        self.assertEqual(pos.heading, 1.57)

    def test_map_matched_object_instantiation(self):
        """Test instantiation of the map-matched Object dataclass."""
        enu_pos = ENUObjectPosition(self.enu_point, 1.57, self.geo_point, self.dimension)
        obj = MapMatchedObject(enu_position=enu_pos)
        self.assertIsInstance(obj, MapMatchedObject)
        self.assertIsInstance(obj.map_matched_bounding_box, MapMatchedObjectBoundingBox)


if __name__ == '__main__':
    unittest.main()