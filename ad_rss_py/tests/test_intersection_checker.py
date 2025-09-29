import unittest
from ad_rss_py.structured.intersection_checker import RssIntersectionConstellationChecker
from ad_rss_py.core.types import (
    RelativeConstellation,
    RelativePosition,
    RelativeObjectState,
    StructuredObjectState,
    LongitudinalRelativePosition,
    LateralRelativePosition,
)
from ad_rss_py.world.types import (
    ObjectType,
    ConstellationType,
    RssDynamics,
)
from ad_rss_py.state.types import LongitudinalResponse
from ad_rss_py.physics.types import Distance, Speed, MetricRange


class TestRssIntersectionConstellationChecker(unittest.TestCase):

    def setUp(self):
        """Set up common objects for the tests."""
        self.checker = RssIntersectionConstellationChecker()

        # Create a default constellation that can be modified by each test
        self.ego_dynamics = RssDynamics(
            alpha_lon_accel_max=2.0, alpha_lon_brake_min=4.0, alpha_lon_brake_max=8.0,
            alpha_lat_accel_max=0.2, alpha_lat_brake_min=0.8, lateral_fluctuation_margin=0.1, response_time=1.0
        )
        self.other_dynamics = self.ego_dynamics

        self.ego_structured_state = StructuredObjectState(
            is_in_correct_lane=True, has_priority=True, distance_to_enter_intersection=Distance(10),
            distance_to_leave_intersection=Distance(20), velocity=Speed(10)
        )
        self.other_structured_state = StructuredObjectState(
            is_in_correct_lane=True, has_priority=False, distance_to_enter_intersection=Distance(15),
            distance_to_leave_intersection=Distance(25), velocity=Speed(10)
        )

        self.ego_state = RelativeObjectState(
            object_type=ObjectType.EgoVehicle, dynamics=self.ego_dynamics,
            structured_object_state=self.ego_structured_state,
            position=MetricRange(minimum=0.0, maximum=4.0)
        )
        self.other_state = RelativeObjectState(
            object_type=ObjectType.OtherVehicle, dynamics=self.other_dynamics,
            structured_object_state=self.other_structured_state,
            position=MetricRange(minimum=10.0, maximum=14.0)
        )

        self.relative_position = RelativePosition(
            longitudinal_position=LongitudinalRelativePosition.InFront, longitudinal_distance=Distance(30),
            lateral_position=LateralRelativePosition.AtLeft, lateral_distance=Distance(5)
        )

    def test_ego_has_priority(self):
        """
        Test the case where the ego vehicle has priority at the intersection.
        """
        constellation = RelativeConstellation(
            constellation_id=1, ego_id=1, object_id=2,
            constellation_type=ConstellationType.IntersectionEgoHasPriority,
            relative_position=self.relative_position,
            ego_state=self.ego_state, other_state=self.other_state
        )

        rss_state = self.checker.calculate_rss_state_intersection(0, constellation)
        self.assertTrue(rss_state.longitudinal_state.is_safe)
        self.assertEqual(rss_state.longitudinal_state.response, LongitudinalResponse.None_)

    def test_object_has_priority(self):
        """
        Test the case where the other object has priority at the intersection.
        """
        constellation = RelativeConstellation(
            constellation_id=2, ego_id=1, object_id=2,
            constellation_type=ConstellationType.IntersectionObjectHasPriority,
            relative_position=self.relative_position,
            ego_state=self.ego_state, other_state=self.other_state
        )

        rss_state = self.checker.calculate_rss_state_intersection(0, constellation)
        self.assertFalse(rss_state.longitudinal_state.is_safe)
        self.assertEqual(rss_state.longitudinal_state.response, LongitudinalResponse.BrakeMin)

    def test_same_priority(self):
        """
        Test the case where both vehicles have the same priority (e.g., a four-way stop).
        """
        constellation = RelativeConstellation(
            constellation_id=3, ego_id=1, object_id=2,
            constellation_type=ConstellationType.IntersectionSamePriority,
            relative_position=self.relative_position,
            ego_state=self.ego_state, other_state=self.other_state
        )

        rss_state = self.checker.calculate_rss_state_intersection(0, constellation)
        self.assertTrue(rss_state.longitudinal_state.is_safe)
        self.assertEqual(rss_state.longitudinal_state.response, LongitudinalResponse.None_)


if __name__ == '__main__':
    unittest.main()