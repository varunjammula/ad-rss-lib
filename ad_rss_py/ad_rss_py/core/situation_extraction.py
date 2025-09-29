from typing import Dict, Tuple
from ..world.types import WorldModel, Constellation, ConstellationType
from ..physics.types import MetricRange, Distance
from .types import (
    RelativeConstellation, RssSituationSnapshot, RelativePosition,
    LongitudinalRelativePosition, LateralRelativePosition,
    RelativeObjectState, StructuredObjectState
)

class RssSituationExtraction:
    def __init__(self):
        self._constellation_id_provider = {}
        self._next_constellation_id = 0

    def _get_constellation_id(self, time_index: int, world_constellation: Constellation) -> int:
        # Simplified constellation ID provider
        key = (world_constellation.ego_vehicle.object_id, world_constellation.object.object_id)
        if key not in self._constellation_id_provider:
            self._constellation_id_provider[key] = self._next_constellation_id
            self._next_constellation_id += 1
        return self._constellation_id_provider[key]

    def extract_situation(self, world_model: WorldModel) -> RssSituationSnapshot:
        snapshot_constellations = {}

        for i, world_constellation in enumerate(world_model.constellations):
            relative_constellation = self._extract_constellation(world_model.time_index, world_constellation, i)

            if relative_constellation:
                const_id = relative_constellation.constellation_id
                if const_id not in snapshot_constellations:
                    snapshot_constellations[const_id] = relative_constellation
                else:
                    # In a real implementation, we would merge constellations.
                    # For now, we'll just keep the first one we see.
                    pass

        return RssSituationSnapshot(
            time_index=world_model.time_index,
            constellations=list(snapshot_constellations.values()),
            default_ego_vehicle_rss_dynamics=world_model.default_ego_vehicle_rss_dynamics
        )

    def _extract_constellation(self, time_index: int, world_constellation: Constellation, world_model_index: int) -> RelativeConstellation:
        # This is a simplified version of extractConstellationInputRangeChecked

        # Basic validation
        if world_constellation.ego_vehicle.object_id == world_constellation.object.object_id:
            # In a real implementation, log an error
            return None

        relative_position, ego_struct_state, other_struct_state = None, None, None

        if world_constellation.constellation_type in [ConstellationType.SameDirection, ConstellationType.OppositeDirection]:
            relative_position, ego_struct_state, other_struct_state = self._convert_objects_non_intersection(world_constellation)
        elif world_constellation.constellation_type in [ConstellationType.IntersectionEgoHasPriority, ConstellationType.IntersectionObjectHasPriority, ConstellationType.IntersectionSamePriority]:
            # Intersection logic is complex and will be implemented later
            return None # Placeholder
        elif world_constellation.constellation_type == ConstellationType.NotRelevant:
            return None # Not relevant constellations are ignored for now

        if relative_position is None:
            return None

        ego_state = RelativeObjectState(
            object_type=world_constellation.ego_vehicle.object_type,
            dynamics=world_constellation.ego_vehicle_rss_dynamics,
            structured_object_state=ego_struct_state
        )
        other_state = RelativeObjectState(
            object_type=world_constellation.object.object_type,
            dynamics=world_constellation.object_rss_dynamics,
            structured_object_state=other_struct_state
        )

        return RelativeConstellation(
            constellation_id=self._get_constellation_id(time_index, world_constellation),
            ego_id=world_constellation.ego_vehicle.object_id,
            object_id=world_constellation.object.object_id,
            constellation_type=world_constellation.constellation_type,
            relative_position=relative_position,
            ego_state=ego_state,
            other_state=other_state,
            world_model_indices=[world_model_index]
        )

    def _convert_objects_non_intersection(self, constellation: Constellation) -> Tuple[RelativePosition, StructuredObjectState, StructuredObjectState]:
        # Simplified version of the C++ logic
        ego_lon_range = constellation.ego_vehicle.state.position
        other_lon_range = constellation.object.state.position

        lon_pos, lon_dist = self._calculate_relative_longitudinal_position(ego_lon_range, other_lon_range)

        # Lateral positions are not fully implemented in this simplified version
        lat_pos, lat_dist = LateralRelativePosition.Overlap, 0.0

        relative_pos = RelativePosition(
            longitudinal_position=lon_pos,
            longitudinal_distance=lon_dist,
            lateral_position=lat_pos,
            lateral_distance=lat_dist
        )

        ego_struct = StructuredObjectState(is_in_correct_lane=True, has_priority=False, distance_to_enter_intersection=0.0, distance_to_leave_intersection=0.0, velocity=constellation.ego_vehicle.state.velocity)
        other_struct = StructuredObjectState(is_in_correct_lane=True, has_priority=False, distance_to_enter_intersection=0.0, distance_to_leave_intersection=0.0, velocity=constellation.object.state.velocity)

        return relative_pos, ego_struct, other_struct

    def _calculate_relative_longitudinal_position(self, ego_metric_range: MetricRange, other_metric_range: MetricRange) -> Tuple[LongitudinalRelativePosition, Distance]:
        if ego_metric_range.minimum > other_metric_range.maximum:
            return LongitudinalRelativePosition.InFront, ego_metric_range.minimum - other_metric_range.maximum
        elif other_metric_range.minimum > ego_metric_range.maximum:
            return LongitudinalRelativePosition.AtBack, other_metric_range.minimum - ego_metric_range.maximum
        else:
            # Overlap cases
            if (ego_metric_range.minimum > other_metric_range.minimum) and (ego_metric_range.maximum > other_metric_range.maximum):
                return LongitudinalRelativePosition.OverlapFront, 0.0
            elif (ego_metric_range.minimum < other_metric_range.minimum) and (ego_metric_range.maximum < other_metric_range.maximum):
                return LongitudinalRelativePosition.OverlapBack, 0.0
            else:
                return LongitudinalRelativePosition.Overlap, 0.0