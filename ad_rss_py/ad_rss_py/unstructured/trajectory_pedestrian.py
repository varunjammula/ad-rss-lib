import math
from typing import Tuple

from ..core.types import RelativeObjectState
from ..geometry.types import Polygon, Point
from ..physics.types import Distance, Angle


class TrajectoryPedestrian:
    """
    Calculates the trajectory sets of a pedestrian.
    """
    max_radius: Distance = Distance(1.0)  # The maximum radius before assuming forward movement
    circle_step_width: Angle = Angle(0.1) # Step width while calculating points on circle (in radians)

    def calculate_trajectory_sets(
        self,
        vehicle_state: RelativeObjectState
    ) -> Tuple[Polygon, Polygon]:
        """
        Calculate the trajectory sets for braking and continue forward behavior.
        """
        # This is a plausible implementation based on the class and method names.
        # The actual C++ implementation may be more complex.

        # For a pedestrian, "braking" means stopping in place. The brake polygon
        # can be represented by a small circle around their current position.
        # For simplicity, we use a single point for now.
        current_pos = vehicle_state.position
        center_x = (current_pos.minimum + current_pos.maximum) / 2.0

        # Since we don't have a lateral position for the pedestrian, we'll assume it's 0 for now.
        # A more complete model would have this information.
        brake_polygon = [Point(x=center_x, y=0.0)]

        # The "continue forward" polygon represents the area the pedestrian could
        # move into. This is modeled as a circle in front of them.
        continue_forward_polygon = []

        # Pedestrian's current heading is needed to project the circle forward.
        # This is not available in the current data model, so we assume a forward direction (0 radians).
        heading = 0.0

        num_steps = int((2 * math.pi) / self.circle_step_width)
        for i in range(num_steps):
            angle = i * self.circle_step_width
            # Parametric equation for a circle
            x = center_x + self.max_radius * math.cos(angle + heading)
            y = 0.0 + self.max_radius * math.sin(angle + heading) # Assuming y starts at 0
            continue_forward_polygon.append(Point(x=x, y=y))

        return brake_polygon, continue_forward_polygon