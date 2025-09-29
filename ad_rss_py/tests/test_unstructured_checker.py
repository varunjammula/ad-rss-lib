import unittest
from unittest.mock import patch

from ad_rss_py.unstructured.unstructured_checker import RssUnstructuredConstellationChecker
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
    TimeIndex,
)
from ad_rss_py.state.types import UnstructuredConstellationResponse, UnstructuredConstellationStateInformation
from ad_rss_py.physics.types import Distance, Speed, MetricRange


class TestRssUnstructuredConstellationChecker(unittest.TestCase):

    def setUp(self):
        """Set up common objects for the tests."""
        self.checker = RssUnstructuredConstellationChecker()

        self.dynamics = RssDynamics(
            alpha_lon_accel_max=2.0, alpha_lon_brake_min=4.0, alpha_lon_brake_max=8.0,
            alpha_lat_accel_max=0.2, alpha_lat_brake_min=0.8, lateral_fluctuation_margin=0.1, response_time=1.0
        )

        self.ego_state = RelativeObjectState(
            object_type=ObjectType.EgoVehicle,
            dynamics=self.dynamics,
            position=MetricRange(minimum=0.0, maximum=4.0),
            structured_object_state=StructuredObjectState(
                is_in_correct_lane=True, has_priority=False,
                distance_to_enter_intersection=Distance(0),
                distance_to_leave_intersection=Distance(0),
                velocity=Speed(15.0)
            )
        )
        self.other_state = RelativeObjectState(
            object_type=ObjectType.OtherVehicle,
            dynamics=self.dynamics,
            position=MetricRange(minimum=20.0, maximum=24.0),
            structured_object_state=StructuredObjectState(
                is_in_correct_lane=True, has_priority=False,
                distance_to_enter_intersection=Distance(0),
                distance_to_leave_intersection=Distance(0),
                velocity=Speed(10.0)
            )
        )

        self.constellation = RelativeConstellation(
            constellation_id=1, ego_id=1, object_id=2,
            constellation_type=ConstellationType.Unstructured,
            relative_position=RelativePosition(
                longitudinal_position=LongitudinalRelativePosition.AtBack,
                longitudinal_distance=Distance(16),
                lateral_position=LateralRelativePosition.Overlap,
                lateral_distance=Distance(0)
            ),
            ego_state=self.ego_state,
            other_state=self.other_state
        )

        self.ego_state_info = UnstructuredConstellationStateInformation(
            brake_trajectory_set=[],
            continue_forward_trajectory_set=[],
            considered_drive_away_steering_angle=0.0
        )

    def test_unstructured_safe_scenario(self):
        """
        Test the safe scenario where polygons do not intersect.
        """
        rss_state = self.checker.calculate_rss_state_unstructured(
            TimeIndex(1), self.constellation, self.ego_state_info
        )

        self.assertTrue(rss_state.unstructured_constellation_state.is_safe)
        self.assertEqual(rss_state.unstructured_constellation_state.response, UnstructuredConstellationResponse.None_)
        self.assertNotEqual(len(self.ego_state_info.brake_trajectory_set), 0)
        self.assertNotEqual(len(self.ego_state_info.continue_forward_trajectory_set), 0)


    @patch.object(RssUnstructuredConstellationChecker, '_polygons_intersect', return_value=True)
    def test_unstructured_unsafe_scenario(self, mock_intersect):
        """
        Test the unsafe scenario by mocking polygon intersection to return True.
        """
        rss_state = self.checker.calculate_rss_state_unstructured(
            TimeIndex(1), self.constellation, self.ego_state_info
        )

        self.assertFalse(rss_state.unstructured_constellation_state.is_safe)
        self.assertEqual(rss_state.unstructured_constellation_state.response, UnstructuredConstellationResponse.Brake)


if __name__ == '__main__':
    unittest.main()