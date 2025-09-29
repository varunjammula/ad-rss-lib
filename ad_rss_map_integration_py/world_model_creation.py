from typing import List
from ad_rss_py.world.types import WorldModel, RssDynamics, TimeIndex, Constellation
from .rss_object_data import RssObjectData
from .map.route.types import FullRoute
from .conversion.object_conversion import RssObjectConversion

# Enums that will be moved to a more appropriate location later
from enum import Enum
class RssRestrictSpeedLimitMode(Enum):
    Unrestricted = 0
    CurrentSpeed = 1
    SpeedLimit = 2

class RssConstellationCreationMode(Enum):
    NotRelevant = 0
    SameDirection = 1
    OppositeDirection = 2
    Intersection = 3

class RssWorldModelCreation:
    """
    Provides supporting functions to create a world model and its constellations.
    """

    def __init__(self, time_index: TimeIndex, default_ego_rss_dynamics: RssDynamics):
        self._world_model = WorldModel(
            time_index=time_index,
            default_ego_vehicle_rss_dynamics=default_ego_rss_dynamics,
            constellations=[]
        )
        self._finalized = False

    def append_constellations(
        self,
        ego_object_data: RssObjectData,
        ego_route: FullRoute,
        other_object_data: RssObjectData,
        restrict_speed_limit_mode: RssRestrictSpeedLimitMode,
        green_traffic_lights: List[int], # Placeholder for LandmarkIdSet
        mode: RssConstellationCreationMode,
        relevant_lanes: List[int] = None # Placeholder for LaneIdSet
    ) -> bool:
        """
        Creates possible constellations between the ego vehicle and another object.
        """
        if self._finalized:
            return False

        # In a real implementation, this method would contain complex logic to:
        # 1. Convert RssObjectData into RssObjectConversion instances.
        # 2. Use a RssWorldModelCreator to analyze routes and intersections.
        # 3. Create and append the appropriate constellations to the world model.

        # For now, we'll just demonstrate the basic flow by creating a placeholder constellation
        ego_conv = RssObjectConversion(ego_object_data)
        other_conv = RssObjectConversion(other_object_data)

        # This is highly simplified. The actual constellation creation is the
        # core of the map integration logic and will be implemented next.
        new_constellation = Constellation(
            constellation_type=mode,
            ego_vehicle=ego_conv.get_rss_object(),
            ego_vehicle_rss_dynamics=ego_conv.get_rss_dynamics(),
            object=other_conv.get_rss_object(),
            object_rss_dynamics=other_conv.get_rss_dynamics(),
            intersecting_road=[], # Placeholder
            ego_vehicle_road=[] # Placeholder
        )
        self._world_model.constellations.append(new_constellation)

        return True

    def get_world_model(self) -> WorldModel:
        """
        Gets the final world model object.
        """
        self._finalized = True
        return self._world_model