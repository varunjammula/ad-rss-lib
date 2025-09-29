from typing import Dict, Tuple

from ..world.types import Constellation, ObjectId, TimeIndex
from ..core.types import RelativeConstellationId


class RssConstellationIdProvider:
    """
    Provides unique and persistent IDs for constellations.
    """

    def __init__(self):
        """
        Initializes the provider with an empty mapping and an ID counter.
        """
        self._id_map: Dict[Tuple[ObjectId, ObjectId], RelativeConstellationId] = {}
        self._next_id: RelativeConstellationId = 0

    def get_constellation_id(self, time_index: TimeIndex, constellation: Constellation) -> RelativeConstellationId:
        """
        Gets a unique, persistent ID for the given constellation.
        """
        # Create a canonical key (sorted tuple) to ensure the ID is consistent
        # regardless of which object is ego.
        obj1_id = constellation.ego_vehicle.object_id
        obj2_id = constellation.object.object_id
        key = tuple(sorted((obj1_id, obj2_id)))

        if key not in self._id_map:
            self._id_map[key] = self._next_id
            self._next_id += 1

        return self._id_map[key]

    def drop_constellation_ids(self, object_id: ObjectId):
        """
        Drops all constellation IDs associated with a given object ID.
        """
        keys_to_remove = [key for key in self._id_map if object_id in key]
        for key in keys_to_remove:
            del self._id_map[key]