from dataclasses import dataclass, field
from enum import Enum
from typing import List

from ..physics.types import Distance, Speed
from ..world.types import ObjectType, ConstellationType, RssDynamics

class LongitudinalRelativePosition(Enum):
    InFront = 0
    AtBack = 1
    Overlap = 2
    OverlapFront = 3
    OverlapBack = 4

class LateralRelativePosition(Enum):
    AtLeft = 0
    AtRight = 1
    Overlap = 2
    OverlapLeft = 3
    OverlapRight = 4

@dataclass
class RelativePosition:
    longitudinal_position: LongitudinalRelativePosition
    longitudinal_distance: Distance
    lateral_position: LateralRelativePosition
    lateral_distance: Distance

@dataclass
class StructuredObjectState:
    is_in_correct_lane: bool
    has_priority: bool
    distance_to_enter_intersection: Distance
    distance_to_leave_intersection: Distance
    velocity: Speed

@dataclass
class RelativeObjectState:
    object_type: ObjectType
    dynamics: RssDynamics
    structured_object_state: StructuredObjectState
    # unstructured_object_state will be added later if needed

@dataclass
class RelativeConstellation:
    constellation_id: int
    ego_id: int
    object_id: int
    constellation_type: ConstellationType
    relative_position: RelativePosition
    ego_state: RelativeObjectState
    other_state: RelativeObjectState
    world_model_indices: List[int] = field(default_factory=list)


@dataclass
class RssSituationSnapshot:
    time_index: int
    constellations: List[RelativeConstellation]
    default_ego_vehicle_rss_dynamics: RssDynamics