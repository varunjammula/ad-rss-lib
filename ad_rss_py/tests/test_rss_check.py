import unittest
from ad_rss_py.core.rss_check import RssCheck
from ad_rss_py.world.types import (
    WorldModel, Constellation, Object, ObjectType, ObjectState, ConstellationType,
    RssDynamics, RoadArea
)
from ad_rss_py.physics.types import MetricRange, Speed
from ad_rss_py.state.types import LongitudinalResponse

class TestRssCheck(unittest.TestCase):

    def setUp(self):
        """Set up common objects for the tests."""
        self.rss_check = RssCheck()

        self.default_rss_dynamics = RssDynamics(
            alpha_lon_accel_max=2.0,
            alpha_lon_brake_min=4.0,
            alpha_lon_brake_max=8.0,
            alpha_lat_accel_max=0.2,
            alpha_lat_brake_min=0.8,
            lateral_fluctuation_margin=0.1,
            response_time=1.0 # Using 1.0s response time for simpler calculation
        )

        self.ego_vehicle = Object(
            object_id=1,
            object_type=ObjectType.EgoVehicle,
            state=ObjectState(
                position=MetricRange(minimum=0.0, maximum=4.0), # 4m long vehicle
                velocity=Speed(30.0)
            )
        )

    def _calculate_expected_safe_dist(self, ego_vel, other_vel):
        # Simplified calculation for this test based on formula
        # d_min = v_r*t_r + 0.5*a_max*t_r^2 + (v_r + t_r*a_max)^2 / (2*b_min) - v_f^2 / (2*b_max)
        t_r = self.default_rss_dynamics.response_time
        a_max = self.default_rss_dynamics.alpha_lon_accel_max
        b_min = self.default_rss_dynamics.alpha_lon_brake_min
        b_max_other = self.default_rss_dynamics.alpha_lon_brake_max

        term1 = ego_vel * t_r
        term2 = 0.5 * a_max * (t_r**2)
        term3 = ((ego_vel + t_r * a_max)**2) / (2 * b_min)
        term4 = (other_vel**2) / (2 * b_max_other)

        return max(0.0, term1 + term2 + term3 - term4)

    def test_safe_situation(self):
        """
        Test a scenario where the ego vehicle is at a safe distance
        from the vehicle in front.
        """
        safe_distance = self._calculate_expected_safe_dist(30.0, 25.0) # ego at 30m/s, other at 25m/s

        # Position other vehicle far ahead, well beyond the safe distance
        other_vehicle_pos_start = self.ego_vehicle.state.position.maximum + safe_distance + 50.0

        other_vehicle = Object(
            object_id=2,
            object_type=ObjectType.OtherVehicle,
            state=ObjectState(
                position=MetricRange(minimum=other_vehicle_pos_start, maximum=other_vehicle_pos_start + 4.0),
                velocity=Speed(25.0)
            )
        )

        constellation = Constellation(
            constellation_type=ConstellationType.SameDirection,
            ego_vehicle=self.ego_vehicle,
            object=other_vehicle,
            ego_vehicle_rss_dynamics=self.default_rss_dynamics,
            object_rss_dynamics=self.default_rss_dynamics,
            ego_vehicle_road=RoadArea(segments=[]),
            intersecting_road=RoadArea(segments=[])
        )

        world_model = WorldModel(
            time_index=1,
            constellations=[constellation],
            default_ego_vehicle_rss_dynamics=self.default_rss_dynamics
        )

        proper_response = self.rss_check.calculate_proper_response(world_model)

        self.assertTrue(proper_response.is_safe)
        self.assertEqual(proper_response.longitudinal_response, LongitudinalResponse.None_)

    def test_unsafe_situation(self):
        """
        Test a scenario where the ego vehicle is too close to the
        vehicle in front, requiring a braking response.
        """
        safe_distance = self._calculate_expected_safe_dist(30.0, 30.0)

        # Position other vehicle close, within the safe distance
        other_vehicle_pos_start = self.ego_vehicle.state.position.maximum + safe_distance - 10.0

        other_vehicle = Object(
            object_id=2,
            object_type=ObjectType.OtherVehicle,
            state=ObjectState(
                position=MetricRange(minimum=other_vehicle_pos_start, maximum=other_vehicle_pos_start + 4.0),
                velocity=Speed(30.0)
            )
        )

        constellation = Constellation(
            constellation_type=ConstellationType.SameDirection,
            ego_vehicle=self.ego_vehicle,
            object=other_vehicle,
            ego_vehicle_rss_dynamics=self.default_rss_dynamics,
            object_rss_dynamics=self.default_rss_dynamics,
            ego_vehicle_road=RoadArea(segments=[]),
            intersecting_road=RoadArea(segments=[])
        )

        world_model = WorldModel(
            time_index=1,
            constellations=[constellation],
            default_ego_vehicle_rss_dynamics=self.default_rss_dynamics
        )

        proper_response = self.rss_check.calculate_proper_response(world_model)

        self.assertFalse(proper_response.is_safe)
        self.assertEqual(proper_response.longitudinal_response, LongitudinalResponse.BrakeMin)
        self.assertIn(other_vehicle.object_id, proper_response.dangerous_objects)
        self.assertEqual(proper_response.acceleration_restrictions.longitudinal_range.maximum, 0.0)

if __name__ == '__main__':
    unittest.main()