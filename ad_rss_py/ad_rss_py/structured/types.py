from dataclasses import dataclass
from ..physics.types import MetricRange

@dataclass
class ObjectDimensions:
    """
    Stores information about an object's position and dimensions.
    """
    longitudinal_dimensions: MetricRange
    lateral_dimensions: MetricRange
    on_positive_lane: bool
    on_negative_lane: bool
    intersection_position: MetricRange