from typing import Dict, Callable, Tuple

from ..core.types import RelativeConstellation
from ..state.types import (
    RssState, UnstructuredRssState, UnstructuredConstellationResponse,
    UnstructuredConstellationStateInformation, LongitudinalRssState, LateralRssState,
    LongitudinalResponse, LateralResponse, RssStateInformation
)
from ..world.types import TimeIndex, ObjectType, ConstellationType
from ..geometry.types import Polygon
from .trajectory_pedestrian import TrajectoryPedestrian
from .trajectory_vehicle import TrajectoryVehicle


class RssUnstructuredConstellationChecker:
    """
    Checks whether an unstructured constellation is safe and determines the proper response.
    """

    def __init__(self):
        """
        Initializes the checker and registers the default trajectory calculators.
        """
        self._trajectory_calculators: Dict[ObjectType, Callable] = {}
        # Register default calculators
        self.register_calculator(ObjectType.EgoVehicle, TrajectoryVehicle())
        self.register_calculator(ObjectType.OtherVehicle, TrajectoryVehicle())
        self.register_calculator(ObjectType.Pedestrian, TrajectoryPedestrian())
        # Other types would be registered here

    def register_calculator(self, object_type: ObjectType, calculator):
        """
        Registers a trajectory calculator for a given object type.
        """
        self._trajectory_calculators[object_type] = calculator

    def _polygons_intersect(self, poly1: Polygon, poly2: Polygon) -> bool:
        """
        Placeholder for polygon intersection logic.
        A real implementation would use a more robust algorithm like SAT.
        For now, we'll just return False to represent the "safe" path.
        """
        # TODO: Implement actual polygon intersection logic
        return False

    def calculate_rss_state_unstructured(
        self,
        time_index: TimeIndex,
        constellation: RelativeConstellation,
        ego_state_info: UnstructuredConstellationStateInformation,
    ) -> RssState:
        """
        Calculates safety checks and determines the required RssState for unstructured constellations.
        """
        ego_calculator = self._trajectory_calculators.get(constellation.ego_state.object_type)
        other_calculator = self._trajectory_calculators.get(constellation.other_state.object_type)

        # Create default safe states for structured checks, as they are not relevant here.
        default_lon_state = LongitudinalRssState(is_safe=True, response=LongitudinalResponse.None_, rss_state_information=RssStateInformation(current_distance=0.0, safe_distance=0.0))
        default_lat_state = LateralRssState(is_safe=True, response=LateralResponse.None_, rss_state_information=RssStateInformation(current_distance=0.0, safe_distance=0.0))

        if not ego_calculator or not other_calculator:
            # Cannot perform check if a calculator is missing
            # In a real implementation, this would be an error.
            # For now, default to safe.
            return RssState(
                constellation_id=constellation.constellation_id,
                object_id=constellation.object_id,
                constellation_type=constellation.constellation_type,
                longitudinal_state=default_lon_state,
                lateral_state_left=default_lat_state,
                lateral_state_right=default_lat_state,
                unstructured_constellation_state=UnstructuredRssState(is_safe=True, response=UnstructuredConstellationResponse.None_)
            )

        ego_brake_poly, ego_continue_poly = ego_calculator.calculate_trajectory_sets(constellation.ego_state)
        other_brake_poly, other_continue_poly = other_calculator.calculate_trajectory_sets(constellation.other_state)

        # Store the calculated trajectories in the output state info
        ego_state_info.brake_trajectory_set = ego_brake_poly
        ego_state_info.continue_forward_trajectory_set = ego_continue_poly

        # Main safety check: Does ego's forward path intersect with the other's brake path?
        is_unsafe = self._polygons_intersect(ego_continue_poly, other_brake_poly)

        response = UnstructuredConstellationResponse.Brake if is_unsafe else UnstructuredConstellationResponse.None_

        unstructured_state = UnstructuredRssState(is_safe=not is_unsafe, response=response)

        return RssState(
            constellation_id=constellation.constellation_id,
            object_id=constellation.object_id,
            constellation_type=constellation.constellation_type,
            longitudinal_state=default_lon_state,
            lateral_state_left=default_lat_state,
            lateral_state_right=default_lat_state,
            unstructured_constellation_state=unstructured_state
        )