from dataclasses import dataclass, field
from typing import List
from enum import Enum

from ad_rss_py.physics.types import Distance, RatioValue, Dimension3D
from ..point.types import ENUPoint, GeoPoint, ECEFPoint, ParaPoint, ENUHeading
from ..lane.types import LaneId

# A value between 0.0 and 1.0 representing certainty.
Probability = float

class MapMatchedPositionType(Enum):
    INVALID = 0
    UNKNOWN = 1
    LANE_IN = 2
    LANE_LEFT = 3
    LANE_RIGHT = 4

@dataclass
class LanePoint:
    """
    Defines a point on a lane with parametric offsets.
    """
    para_point: ParaPoint
    lateral_t: RatioValue
    lane_length: Distance
    lane_width: Distance

@dataclass
class MapMatchedPosition:
    """
    Represents a map-matched position with its confidence and type.
    """
    lane_point: LanePoint
    type: MapMatchedPositionType
    matched_point: ECEFPoint
    query_point: ECEFPoint
    probability: Probability
    matched_point_distance: Distance

MapMatchedPositionConfidenceList = List[MapMatchedPosition]

@dataclass
class LaneOccupiedRegion:
    """
    Represents an occupied region on a lane.
    """
    lane_id: LaneId
    longitudinal_range: "ParametricRange"
    lateral_range: "ParametricRange"

LaneOccupiedRegionList = List[LaneOccupiedRegion]

@dataclass
class MapMatchedObjectBoundingBox:
    """
    Represents the map-matched bounding box of an object.
    """
    lane_occupied_regions: LaneOccupiedRegionList = field(default_factory=list)
    reference_point_positions: List[MapMatchedPositionConfidenceList] = field(default_factory=list)
    sampling_distance: Distance = 0.0
    match_radius: Distance = 0.0

@dataclass
class ENUObjectPosition:
    """
    Represents the position of an object in the ENU coordinate system.
    """
    center_point: ENUPoint
    heading: ENUHeading
    enu_reference_point: GeoPoint
    dimension: Dimension3D

@dataclass
class Object:
    """
    Represents a map-matched object.
    """
    enu_position: ENUObjectPosition
    map_matched_bounding_box: MapMatchedObjectBoundingBox = field(default_factory=MapMatchedObjectBoundingBox)