from ad_rss_py.world.types import Object, RssDynamics, OccupiedRegion, ObjectType, ObjectState
from ad_rss_py.physics.types import Speed, MetricRange, Dimension3D
from ..rss_object_data import RssObjectData
from ..map.route.types import LaneInterval

class RssObjectConversion:
    """
    Provides support to convert ad::map objects into ad::rss objects.
    """

    def __init__(self, object_data: RssObjectData, object_occupied_regions: list = None):
        self._object_data = object_data
        self._rss_object = Object(
            object_id=object_data.id,
            object_type=object_data.type,
            state=ObjectState(
                position=MetricRange(minimum=0.0, maximum=0.0), # Placeholder
                velocity=Speed(0.0), # Placeholder
                dimension=Dimension3D(
                    length=object_data.match_object.enu_position.dimension.length,
                    width=object_data.match_object.enu_position.dimension.width,
                    height=object_data.match_object.enu_position.dimension.height
                ),
                occupied_regions=object_occupied_regions if object_occupied_regions else []
            )
        )
        self._max_speed_on_acceleration = object_data.speed_range.maximum

    def get_rss_dynamics(self) -> RssDynamics:
        """
        Returns the RssDynamics of the object, with the speed limit updated.
        """
        dynamics = self._object_data.rss_dynamics
        dynamics.max_speed_on_acceleration = self._max_speed_on_acceleration
        return dynamics

    def get_rss_object(self) -> Object:
        """
        Returns the RSS Object description.
        """
        return self._rss_object

    def get_id(self) -> int:
        """
        Returns the object's ID.
        """
        return self._rss_object.object_id

    def update_speed_limit(self, max_speed_on_acceleration: Speed):
        """
        Updates the max speed content.
        """
        self._max_speed_on_acceleration = max_speed_on_acceleration

    def lane_interval_added(self, lane_interval: LaneInterval):
        """
        Adds a relevant occupied region when a lane interval is added to the object's route.
        """
        # This is a simplified logic. A real implementation would perform
        # complex geometric calculations to determine the exact occupied region.
        new_occupied_region = OccupiedRegion(
            segment_id=lane_interval.lane_id,
            lon_range=ParametricRange(minimum=lane_interval.start, maximum=lane_interval.end),
            lat_range=ParametricRange(minimum=0.0, maximum=1.0) # Assume it occupies the full lateral width
        )
        self._rss_object.state.occupied_regions.append(new_occupied_region)