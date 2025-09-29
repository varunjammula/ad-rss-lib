from dataclasses import dataclass
from enum import Enum
from typing import List

from ..physics.types import Distance, Speed, Acceleration, MetricRange, ParametricRange, Dimension3D


class ObjectType(Enum):
    EgoVehicle = 0
    OtherVehicle = 1
    Pedestrian = 2
    Bicycle = 3
    OtherObject = 4
    ArtificialObject = 5
    ArtificialPedestrian = 6
    ArtificialVehicle = 7


class ConstellationType(Enum):
    NotRelevant = 0
    SameDirection = 1
    OppositeDirection = 2
    IntersectionEgoHasPriority = 3
    IntersectionObjectHasPriority = 4
    IntersectionSamePriority = 5
    Unstructured = 6


class LaneDrivingDirection(Enum):
    Bidirectional = 0
    Positive = 1
    Negative = 2


LaneSegmentId = int


ObjectId = int


TimeIndex = int


class RoadSegmentType(Enum):
    Normal = 0
    Intersection = 1


@dataclass
class RoadSegment:
    """
    Defines a road segment.
    """
    type: RoadSegmentType
    lane_segments: List["LaneSegment"]
    minimum_length_after_intersecting_area: Distance
    minimum_length_before_intersecting_area: Distance


@dataclass
class LaneSegment:
    """
    Defines a lane segment.
    """
    id: LaneSegmentId
    driving_direction: LaneDrivingDirection
    length: MetricRange
    width: MetricRange


@dataclass
class LateralRssAccelerationValues:
    """
    Collection of the RSS acceleration values in lateral direction.
    """
    accel_max: Acceleration
    brake_min: Acceleration


@dataclass
class LongitudinalRssAccelerationValues:
    """
    Collection of the RSS acceleration values in longitudinal direction.
    """
    accel_max: Acceleration
    brake_max: Acceleration
    brake_min: Acceleration
    brake_min_correct: Acceleration


@dataclass
class RssDynamics:
    alpha_lon_accel_max: Acceleration
    alpha_lon_brake_min: Acceleration
    alpha_lon_brake_max: Acceleration
    alpha_lat_accel_max: Acceleration
    alpha_lat_brake_min: Acceleration
    lateral_fluctuation_margin: Distance
    response_time: float


from dataclasses import field

@dataclass
class ObjectState:
    position: MetricRange
    velocity: Speed
    dimension: Dimension3D
    occupied_regions: List["OccupiedRegion"] = field(default_factory=list)


@dataclass
class Object:
    object_id: int
    object_type: ObjectType
    state: ObjectState


@dataclass
class RoadArea:
    segments: List[MetricRange]


@dataclass
class Constellation:
    constellation_type: ConstellationType
    ego_vehicle: Object
    ego_vehicle_rss_dynamics: RssDynamics
    object: Object
    object_rss_dynamics: RssDynamics
    intersecting_road: RoadArea
    ego_vehicle_road: RoadArea


@dataclass
class WorldModel:
    time_index: int
    default_ego_vehicle_rss_dynamics: RssDynamics
    constellations: List[Constellation]


@dataclass
class OccupiedRegion:
    """
    Describes the region that an object covers within a lane segment.
    """
    segment_id: LaneSegmentId
    lon_range: ParametricRange
    lat_range: ParametricRange