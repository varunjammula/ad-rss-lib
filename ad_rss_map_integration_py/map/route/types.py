from typing import List
from dataclasses import dataclass, field
from enum import Enum
from ad_rss_py.physics.types import ParametricValue
from ..lane.types import LaneId, LaneIdList
from ..point.types import BoundingSphere

RouteLaneOffset = int
SegmentCounter = int
RoutePlanningCounter = int


class RouteCreationMode(Enum):
    Undefined = 0
    SameDrivingDirection = 1
    AllRoutableLanes = 2
    AllNeighborLanes = 3


@dataclass
class LaneInterval:
    """
    Defines an interval on a lane.
    """
    lane_id: LaneId
    start: ParametricValue
    end: ParametricValue
    wrong_way: bool = False


@dataclass
class LaneSegment:
    """
    Defines a segment of a lane within a route.
    """
    left_neighbor: LaneId
    right_neighbor: LaneId
    predecessors: LaneIdList
    successors: LaneIdList
    lane_interval: LaneInterval
    route_lane_offset: RouteLaneOffset

LaneSegmentList = List[LaneSegment]


@dataclass
class RoadSegment:
    """
    Defines a segment of a road containing parallel lanes.
    """
    drivable_lane_segments: LaneSegmentList
    segment_count_from_destination: SegmentCounter
    bounding_sphere: BoundingSphere

RoadSegmentList = List[RoadSegment]


@dataclass
class FullRoute:
    """
    Defines a route along a road.
    """
    road_segments: RoadSegmentList
    route_planning_counter: RoutePlanningCounter = 0
    full_route_segment_count: SegmentCounter = 0
    destination_lane_offset: RouteLaneOffset = 0
    min_lane_offset: RouteLaneOffset = 0
    max_lane_offset: RouteLaneOffset = 0
    route_creation_mode: RouteCreationMode = RouteCreationMode.Undefined