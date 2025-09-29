import unittest
from ad_rss_map_integration_py.map.point.types import (
    ECEFPoint,
    BoundingSphere,
    ECEFCoordinate,
)
from ad_rss_py.physics.types import Distance


class TestPointTypes(unittest.TestCase):

    def test_ecef_point_instantiation(self):
        """
        Test that the ECEFPoint dataclass can be instantiated.
        """
        point = ECEFPoint(
            x=ECEFCoordinate(1.0),
            y=ECEFCoordinate(2.0),
            z=ECEFCoordinate(3.0)
        )
        self.assertIsInstance(point, ECEFPoint)
        self.assertEqual(point.x, 1.0)

    def test_bounding_sphere_instantiation(self):
        """
        Test that the BoundingSphere dataclass can be instantiated.
        """
        center_point = ECEFPoint(x=1.0, y=2.0, z=3.0)
        radius = Distance(10.0)

        sphere = BoundingSphere(center=center_point, radius=radius)
        self.assertIsInstance(sphere, BoundingSphere)
        self.assertEqual(sphere.center, center_point)
        self.assertEqual(sphere.radius, 10.0)

if __name__ == '__main__':
    unittest.main()