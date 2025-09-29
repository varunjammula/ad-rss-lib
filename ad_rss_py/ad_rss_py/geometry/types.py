from dataclasses import dataclass
from ..physics.types import Distance

@dataclass
class Point:
    """
    Represents a 2D point in a Cartesian coordinate system.
    """
    x: Distance
    y: Distance