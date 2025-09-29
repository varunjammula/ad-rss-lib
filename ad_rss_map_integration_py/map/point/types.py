from dataclasses import dataclass
from ad_rss_py.physics.types import Distance, ParametricValue
from ..lane.types import LaneId

# Base coordinate and geometric types from ad::map::point
Longitude = float
Latitude = float
Altitude = float
ENUCoordinate = float
ENUHeading = float

@dataclass
class GeoPoint:
    """
    Represents a geographical location in WGS-84.
    """
    longitude: Longitude
    latitude: Latitude
    altitude: Altitude

@dataclass
class ENUPoint:
    """
    Represents a point in the ENU (East, North, Up) coordinate system.
    """
    x: ENUCoordinate
    y: ENUCoordinate
    z: ENUCoordinate

@dataclass
class ECEFPoint:
    """
    Represents a point in the ECEF (Earth-Centered, Earth-Fixed) coordinate system.
    """
    x: "ECEFCoordinate"
    y: "ECEFCoordinate"
    z: "ECEFCoordinate"

@dataclass
class BoundingSphere:
    """
    Represents a bounding sphere with a center point and a radius.
    """
    center: ECEFPoint
    radius: Distance

@dataclass
class ParaPoint:
    """
    Defines a parametric point on a lane of the map.
    """
    lane_id: LaneId
    parametric_offset: ParametricValue

# Forward-declare ECEFCoordinate as it's used by ECEFPoint
ECEFCoordinate = float