import unittest
import math

from ad_rss_py.unstructured.trajectory_pedestrian import TrajectoryPedestrian
from ad_rss_py.unstructured.trajectory_vehicle import TrajectoryVehicle
from ad_rss_py.core.types import RelativeObjectState, StructuredObjectState
from ad_rss_py.world.types import ObjectType, RssDynamics
from ad_rss_py.physics.types import MetricRange, Distance, Speed, Acceleration


class TestUnstructuredLogic(unittest.TestCase):

    def setUp(self):
        """Set up common dynamics for tests."""
        self.dynamics = RssDynamics(
            alpha_lon_accel_max=Acceleration(2.0),
            alpha_lon_brake_min=Acceleration(4.0),
            alpha_lon_brake_max=Acceleration(8.0),
            alpha_lat_accel_max=Acceleration(0.2),
            alpha_lat_brake_min=Acceleration(0.8),
            lateral_fluctuation_margin=Distance(0.1),
            response_time=1.0
        )

    def test_trajectory_pedestrian(self):
        """
        Test the trajectory calculation for a pedestrian.
        """
        pedestrian_state = RelativeObjectState(
            object_type=ObjectType.Pedestrian,
            dynamics=self.dynamics,
            position=MetricRange(minimum=10.0, maximum=10.5),
            structured_object_state=StructuredObjectState(
                is_in_correct_lane=True, has_priority=False,
                distance_to_enter_intersection=Distance(0),
                distance_to_leave_intersection=Distance(0),
                velocity=Speed(1.5) # Walking speed
            )
        )

        ped_trajectory_calc = TrajectoryPedestrian()
        brake_poly, continue_poly = ped_trajectory_calc.calculate_trajectory_sets(pedestrian_state)

        # Brake polygon should be a single point at the pedestrian's center
        self.assertEqual(len(brake_poly), 1)
        self.assertAlmostEqual(brake_poly[0].x, 10.25)

        # Continue forward polygon should be a circle
        expected_points = int((2 * math.pi) / TrajectoryPedestrian.circle_step_width)
        self.assertEqual(len(continue_poly), expected_points)
        # Check a point on the circle (e.g., directly in front)
        expected_x = 10.25 + TrajectoryPedestrian.max_radius
        self.assertAlmostEqual(continue_poly[0].x, expected_x)


    def test_trajectory_vehicle(self):
        """
        Test the trajectory calculation for a vehicle.
        """
        vehicle_state = RelativeObjectState(
            object_type=ObjectType.OtherVehicle,
            dynamics=self.dynamics,
            position=MetricRange(minimum=5.0, maximum=10.0),
            structured_object_state=StructuredObjectState(
                is_in_correct_lane=True, has_priority=False,
                distance_to_enter_intersection=Distance(0),
                distance_to_leave_intersection=Distance(0),
                velocity=Speed(20.0) # 20 m/s
            )
        )

        veh_trajectory_calc = TrajectoryVehicle()
        brake_poly, continue_poly = veh_trajectory_calc.calculate_trajectory_sets(vehicle_state)

        # --- Test Brake Polygon ---
        # d = v^2 / (2*a) = 20^2 / (2*4) = 400 / 8 = 50m
        self.assertEqual(len(brake_poly), 4)
        # Check front-right corner of brake polygon
        self.assertAlmostEqual(brake_poly[2].x, 10.0 + 50.0) # end of vehicle + brake_dist
        self.assertAlmostEqual(brake_poly[2].y, 1.8 / 2) # half of assumed width

        # --- Test Continue Forward Polygon ---
        # d = v*t + 0.5*a*t^2 = 20*1 + 0.5*2*1^2 = 20 + 1 = 21m
        self.assertEqual(len(continue_poly), 4)
        # Check front-right corner of continue polygon
        self.assertAlmostEqual(continue_poly[2].x, 10.0 + 21.0) # end of vehicle + continue_dist
        self.assertAlmostEqual(continue_poly[2].y, 1.8 / 2)


if __name__ == '__main__':
    unittest.main()