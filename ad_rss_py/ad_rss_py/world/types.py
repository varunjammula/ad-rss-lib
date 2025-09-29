from dataclasses import dataclass
from enum import Enum
from typing import List

from ..physics.types import Distance, Speed, Acceleration, MetricRange


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


@dataclass
class RssDynamics:
    alpha_lon_accel_max: Acceleration
    alpha_lon_brake_min: Acceleration
    alpha_lon_brake_max: Acceleration
    alpha_lat_accel_max: Acceleration
    alpha_lat_brake_min: Acceleration
    lateral_fluctuation_margin: Distance
    response_time: float


@dataclass
class ObjectState:
    position: MetricRange
    velocity: Speed
    # Other fields from the C++ ObjectState might be added here


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