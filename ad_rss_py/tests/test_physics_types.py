import unittest
from ad_rss_py.physics.types import ParametricRange, ParametricValue

class TestPhysicsTypes(unittest.TestCase):

    def test_parametric_range_instantiation(self):
        """
        Test that the ParametricRange dataclass can be instantiated.
        """
        min_val = ParametricValue(0.2)
        max_val = ParametricValue(0.8)

        parametric_range = ParametricRange(minimum=min_val, maximum=max_val)

        self.assertIsInstance(parametric_range, ParametricRange)
        self.assertEqual(parametric_range.minimum, min_val)
        self.assertEqual(parametric_range.maximum, max_val)

if __name__ == '__main__':
    unittest.main()