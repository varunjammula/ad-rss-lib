from typing import Tuple

from ..core.types import RelativeObjectState
from ..geometry.types import Polygon, Point
from ..physics.types import Distance


class TrajectoryVehicle:
    """
    Calculates the trajectory sets of a vehicle.
    """

    def calculate_trajectory_sets(
        self,
        vehicle_state: RelativeObjectState
    ) -> Tuple[Polygon, Polygon]:
        """
        Calculate the trajectory sets for braking and continue forward behavior.
        """
        # This is a plausible implementation based on the class and method names.
        # It calculates simple rectangular polygons for the vehicle's path.

        v = vehicle_state.structured_object_state.velocity
        response_time = vehicle_state.dynamics.response_time
        brake_min = vehicle_state.dynamics.alpha_lon_brake_min
        accel_max = vehicle_state.dynamics.alpha_lon_accel_max

        current_pos = vehicle_state.position
        vehicle_length = current_pos.maximum - current_pos.minimum
        vehicle_width = Distance(1.8) # Assume a standard vehicle width

        # --- Brake Polygon ---
        # d = v^2 / (2*a)
        brake_dist = (v**2) / (2 * brake_min) if brake_min > 0 else 0.0

        # Polygon is a rectangle from current pos to brake_dist forward
        bl_brake = Point(x=current_pos.minimum, y=-vehicle_width/2)
        br_brake = Point(x=current_pos.minimum, y=vehicle_width/2)
        fl_brake = Point(x=current_pos.maximum + brake_dist, y=-vehicle_width/2)
        fr_brake = Point(x=current_pos.maximum + brake_dist, y=vehicle_width/2)
        brake_polygon = [bl_brake, br_brake, fr_brake, fl_brake]


        # --- Continue Forward Polygon ---
        # d = v*t + 0.5*a*t^2
        continue_dist = (v * response_time) + (0.5 * accel_max * response_time**2)

        bl_cont = Point(x=current_pos.minimum, y=-vehicle_width/2)
        br_cont = Point(x=current_pos.minimum, y=vehicle_width/2)
        fl_cont = Point(x=current_pos.maximum + continue_dist, y=-vehicle_width/2)
        fr_cont = Point(x=current_pos.maximum + continue_dist, y=vehicle_width/2)
        continue_forward_polygon = [bl_cont, br_cont, fr_cont, fl_cont]

        return brake_polygon, continue_forward_polygon