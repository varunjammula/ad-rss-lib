from enum import Enum
from typing import List, Tuple
import math

from .types import ObjectDimensions
from ..world.types import OccupiedRegion, RoadSegment, LaneSegment, LaneDrivingDirection
from ..physics.types import MetricRange, Distance


class RssObjectPositionExtractor:
    """
    Calculates object positions based on a series of road and lane segments.
    """

    class IntersectionState(Enum):
        BeforeIntersection = 0
        WithinIntersection = 1
        AfterIntersection = 2

    def __init__(self, occupied_regions: List[OccupiedRegion]):
        self._occupied_regions = list(occupied_regions)
        self._object_dimensions = ObjectDimensions(
            longitudinal_dimensions=MetricRange(minimum=Distance(math.inf), maximum=Distance(-math.inf)),
            lateral_dimensions=MetricRange(minimum=Distance(math.inf), maximum=Distance(-math.inf)),
            on_positive_lane=False,
            on_negative_lane=False,
            intersection_position=MetricRange(minimum=Distance(0.0), maximum=Distance(0.0))
        )
        self._intersection_state = self.IntersectionState.BeforeIntersection
        self._current_longitudinal_road_segment_start = MetricRange(minimum=0.0, maximum=0.0)
        self._road_segment_min_length_after_intersecting_area = Distance(0.0)

    def new_road_segment(self, longitudinal_start: MetricRange, road_segment: RoadSegment) -> bool:
        """
        Indicates that there is a new road segment.
        """
        self._current_longitudinal_road_segment_start = longitudinal_start
        self._road_segment_min_length_after_intersecting_area = road_segment.minimum_length_after_intersecting_area
        return True

    def new_lane_segment(self, lateral_distance: MetricRange, lane_segment: LaneSegment) -> bool:
        """
        Adds information of the next adjacent lane segment and processes it.
        """
        regions_in_lane = [r for r in self._occupied_regions if r.segment_id == lane_segment.id]

        for region in regions_in_lane:
            # Update longitudinal dimensions
            lon_min = self._current_longitudinal_road_segment_start.minimum + (lane_segment.length.minimum * region.lon_range.minimum)
            lon_max = self._current_longitudinal_road_segment_start.minimum + (lane_segment.length.minimum * region.lon_range.maximum)

            self._object_dimensions.longitudinal_dimensions.minimum = min(self._object_dimensions.longitudinal_dimensions.minimum, lon_min)
            self._object_dimensions.longitudinal_dimensions.maximum = max(self._object_dimensions.longitudinal_dimensions.maximum, lon_max)

            # Update lateral dimensions
            lat_min = lateral_distance.minimum + (lane_segment.width.minimum * region.lat_range.minimum)
            lat_max = lateral_distance.minimum + (lane_segment.width.minimum * region.lat_range.maximum)

            self._object_dimensions.lateral_dimensions.minimum = min(self._object_dimensions.lateral_dimensions.minimum, lat_min)
            self._object_dimensions.lateral_dimensions.maximum = max(self._object_dimensions.lateral_dimensions.maximum, lat_max)

            # Update lane direction flags
            if lane_segment.driving_direction == LaneDrivingDirection.Positive:
                self._object_dimensions.on_positive_lane = True
            elif lane_segment.driving_direction == LaneDrivingDirection.Negative:
                self._object_dimensions.on_negative_lane = True

            # Simplified intersection logic will be added later if needed

            self._occupied_regions.remove(region)

        return True

    def get_object_dimensions(self) -> Tuple[bool, ObjectDimensions]:
        """
        Retrieve the object dimension information.
        Returns a tuple of (is_complete, dimensions).
        """
        is_complete = not self._occupied_regions
        return (is_complete, self._object_dimensions)