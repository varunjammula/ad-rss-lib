from dataclasses import dataclass

# Basic physical types
Distance = float
Duration = float
Speed = float
Acceleration = float
Angle = float

@dataclass
class MetricRange:
    minimum: Distance
    maximum: Distance