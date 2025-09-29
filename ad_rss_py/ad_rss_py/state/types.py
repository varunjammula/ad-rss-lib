from dataclasses import dataclass, field
from enum import Enum
from typing import List

from ..physics.types import Acceleration, Distance
from ..world.types import RssDynamics, ConstellationType


class LongitudinalResponse(Enum):
    None_ = 0  # "None" is a keyword in Python
    BrakeMin = 1
    BrakeMinCorrect = 2


class LateralResponse(Enum):
    None_ = 0
    BrakeMin = 1


class UnstructuredConstellationResponse(Enum):
    None_ = 0
    Brake = 1
    DriveAway = 2


@dataclass
class RssStateInformation:
    current_distance: Distance
    safe_distance: Distance


@dataclass
class LongitudinalRssState:
    is_safe: bool
    response: LongitudinalResponse
    rss_state_information: RssStateInformation


@dataclass
class LateralRssState:
    is_safe: bool
    response: LateralResponse
    rss_state_information: RssStateInformation


@dataclass
class UnstructuredRssState:
    is_safe: bool
    response: UnstructuredConstellationResponse


@dataclass
class RssState:
    constellation_id: int
    object_id: int
    constellation_type: ConstellationType
    longitudinal_state: LongitudinalRssState
    lateral_state_left: LateralRssState
    lateral_state_right: LateralRssState
    unstructured_constellation_state: UnstructuredRssState


@dataclass
class AccelerationRestriction:
    longitudinal_range: "MetricRange"
    lateral_left_range: "MetricRange"
    lateral_right_range: "MetricRange"


@dataclass
class ProperResponse:
    time_index: int
    is_safe: bool
    dangerous_objects: List[int] = field(default_factory=list)
    longitudinal_response: LongitudinalResponse = LongitudinalResponse.None_
    lateral_response_left: LateralResponse = LateralResponse.None_
    lateral_response_right: LateralResponse = LateralResponse.None_
    unstructured_constellation_response: UnstructuredConstellationResponse = UnstructuredConstellationResponse.None_
    acceleration_restrictions: AccelerationRestriction = None


@dataclass
class RssStateSnapshot:
    time_index: int
    individual_responses: List[RssState] = field(default_factory=list)
    default_ego_vehicle_rss_dynamics: RssDynamics = None