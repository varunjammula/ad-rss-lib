from dataclasses import dataclass
from datetime import datetime

from ad_rss_py.world.types import ObjectId, ObjectType, RssDynamics
from ad_rss_py.physics.types import SpeedRange, AngularVelocity, Angle
from .map.match.types import Object as MapMatchedObject


@dataclass
class RssObjectData:
    """
    Data structure containing all relevant information about an object
    for the map integration and RSS processing.
    """
    last_update: datetime
    id: ObjectId
    type: ObjectType
    match_object: MapMatchedObject
    speed_range: SpeedRange
    yaw_rate: AngularVelocity
    steering_angle: Angle
    rss_dynamics: RssDynamics