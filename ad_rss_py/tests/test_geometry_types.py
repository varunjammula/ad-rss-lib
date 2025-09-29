import unittest
from ad_rss_py.geometry.types import Point
from ad_rss_py.physics.types import Distance

class TestGeometryTypes(unittest.TestCase):

    def test_point_instantiation(self):
        """
        Test that the Point dataclass can be instantiated.
        """
        x_coord = Distance(10.0)
        y_coord = Distance(20.5)

        point = Point(x=x_coord, y=y_coord)

        self.assertIsInstance(point, Point)
        self.assertEqual(point.x, x_coord)
        self.assertEqual(point.y, y_coord)

if __name__ == '__main__':
    unittest.main()