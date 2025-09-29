import unittest
from ad_rss_py.unstructured.types import (
    TrajectoryPoint,
    TrajectorySetStep,
    TrafficParticipantLocation,
    TrajectorySetStepVehicleLocation,
)
from ad_rss_py.geometry.types import Point
from ad_rss_py.physics.types import Distance, Angle, Duration


class TestUnstructuredTypes(unittest.TestCase):

    def test_trajectory_point_instantiation(self):
        """
        Test that the TrajectoryPoint dataclass can be instantiated.
        """
        point = TrajectoryPoint(
            px=Distance(1.0),
            py=Distance(2.0),
            heading=Angle(0.5),
            time_stamp=Duration(10.0)
        )
        self.assertIsInstance(point, TrajectoryPoint)
        self.assertEqual(point.px, 1.0)
        self.assertEqual(point.py, 2.0)
        self.assertEqual(point.heading, 0.5)
        self.assertEqual(point.time_stamp, 10.0)

    def test_trajectory_set_step_instantiation(self):
        """
        Test that the TrajectorySetStep dataclass can be instantiated.
        """
        center_point = TrajectoryPoint(px=Distance(1.0), py=Distance(2.0), heading=Angle(0.5), time_stamp=Duration(10.0))
        left_point = TrajectoryPoint(px=Distance(0.0), py=Distance(2.0), heading=Angle(0.5), time_stamp=Duration(10.0))
        right_point = TrajectoryPoint(px=Distance(2.0), py=Distance(2.0), heading=Angle(0.5), time_stamp=Duration(10.0))

        trajectory_set_step = TrajectorySetStep(
            left=[left_point],
            right=[right_point],
            center=center_point
        )
        self.assertIsInstance(trajectory_set_step, TrajectorySetStep)
        self.assertEqual(trajectory_set_step.center, center_point)
        self.assertEqual(trajectory_set_step.left, [left_point])
        self.assertEqual(trajectory_set_step.right, [right_point])


    def test_traffic_participant_location_instantiation(self):
        """
        Test that the TrafficParticipantLocation dataclass can be instantiated.
        """
        front_left = Point(x=Distance(1.0), y=Distance(3.0))
        front_right = Point(x=Distance(3.0), y=Distance(3.0))
        back_left = Point(x=Distance(1.0), y=Distance(1.0))
        back_right = Point(x=Distance(3.0), y=Distance(1.0))

        location = TrafficParticipantLocation(
            front_left=front_left,
            front_right=front_right,
            back_left=back_left,
            back_right=back_right
        )
        self.assertIsInstance(location, TrafficParticipantLocation)
        self.assertEqual(location.front_left, front_left)


    def test_trajectory_set_step_vehicle_location_instantiation(self):
        """
        Test that the TrajectorySetStepVehicleLocation dataclass can be instantiated.
        """
        center_location = TrafficParticipantLocation(
            front_left=Point(x=1, y=3), front_right=Point(x=3, y=3),
            back_left=Point(x=1, y=1), back_right=Point(x=3, y=1)
        )
        left_location = TrafficParticipantLocation(
            front_left=Point(x=0, y=3), front_right=Point(x=2, y=3),
            back_left=Point(x=0, y=1), back_right=Point(x=2, y=1)
        )
        right_location = TrafficParticipantLocation(
            front_left=Point(x=2, y=3), front_right=Point(x=4, y=3),
            back_left=Point(x=2, y=1), back_right=Point(x=4, y=1)
        )

        vehicle_location = TrajectorySetStepVehicleLocation(
            left=left_location,
            right=right_location,
            center=center_location
        )
        self.assertIsInstance(vehicle_location, TrajectorySetStepVehicleLocation)
        self.assertEqual(vehicle_location.center, center_location)

if __name__ == '__main__':
    unittest.main()