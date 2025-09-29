from typing import List

from .rss_object_data import RssObjectData
from .map.route.types import FullRoute, ConnectingRoute
from .conversion.object_conversion import RssObjectConversion
from .world_model_creation import RssWorldModelCreation, RssRestrictSpeedLimitMode

# Placeholder for a C++ map intersection pointer
class Intersection:
    pass

class RssWorldModelCreator:
    """
    Provides support to create the RSS world model and append RSS Constellations.
    """

    def __init__(self,
                 restrict_speed_limit_mode: RssRestrictSpeedLimitMode,
                 green_traffic_lights: List[int], # Placeholder for LandmarkIdSet
                 world_model_creation: RssWorldModelCreation):
        self._restrict_speed_limit_mode = restrict_speed_limit_mode
        self._green_traffic_lights = green_traffic_lights
        self._world_model_creation = world_model_creation

    def append_not_relevant_constellation(self, route: FullRoute, ego_object: RssObjectConversion, other_object: RssObjectConversion) -> bool:
        # Placeholder
        return True

    def append_non_intersection_constellation(self, connecting_route: "ConnectingRoute", constellation_type, ego_object: RssObjectConversion, other_object: RssObjectConversion) -> bool:
        # Placeholder
        return True

    def append_merging_constellation(self, connecting_route: "ConnectingRoute", constellation_type, ego_object: RssObjectConversion, other_object: RssObjectConversion) -> bool:
        # Placeholder
        return True

    def append_intersection_constellation(self, intersection: Intersection, ego_route: FullRoute, object_route: FullRoute, intersection_other_route: FullRoute, ego_object: RssObjectConversion, other_object: RssObjectConversion) -> bool:
        # Placeholder
        return True

    def append_road_boundary_constellations(self, ego_route: FullRoute, ego_object: RssObjectConversion) -> bool:
        # Placeholder
        return True

    def append_unstructured_constellation(self, ego_object: RssObjectConversion, other_object: RssObjectConversion) -> bool:
        # Placeholder
        return True