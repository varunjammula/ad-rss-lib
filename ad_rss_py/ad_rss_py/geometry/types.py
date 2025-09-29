from dataclasses import dataclass
from ..physics.types import Distance

from typing import List

@dataclass
class Point:
    """
    Represents a 2D point in a Cartesian coordinate system.
    """
    x: Distance
    y: Distance

Polygon = List[Point]