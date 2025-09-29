import unittest
from ad_rss_py.structured.types import ObjectDimensions
from ad_rss_py.physics.types import MetricRange, Distance

class TestStructuredTypes(unittest.TestCase):

    def test_object_dimensions_instantiation(self):
        """
        Test that the ObjectDimensions dataclass can be instantiated.
        """
        lon_dims = MetricRange(minimum=Distance(0.0), maximum=Distance(5.0))
        lat_dims = MetricRange(minimum=Distance(-1.0), maximum=Distance(1.0))
        intersect_pos = MetricRange(minimum=Distance(10.0), maximum=Distance(20.0))

        obj_dims = ObjectDimensions(
            longitudinal_dimensions=lon_dims,
            lateral_dimensions=lat_dims,
            on_positive_lane=True,
            on_negative_lane=False,
            intersection_position=intersect_pos
        )

        self.assertIsInstance(obj_dims, ObjectDimensions)
        self.assertEqual(obj_dims.longitudinal_dimensions, lon_dims)
        self.assertEqual(obj_dims.lateral_dimensions, lat_dims)
        self.assertTrue(obj_dims.on_positive_lane)
        self.assertFalse(obj_dims.on_negative_lane)
        self.assertEqual(obj_dims.intersection_position, intersect_pos)

if __name__ == '__main__':
    unittest.main()