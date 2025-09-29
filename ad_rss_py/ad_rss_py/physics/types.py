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

ParametricValue = float

@dataclass
class ParametricRange:
    minimum: ParametricValue
    maximum: ParametricValue

AngularVelocity = float
RatioValue = float

@dataclass
class SpeedRange:
    """
    A speed range described by its borders: [minimum, maximum].
    """
    minimum: Speed
    maximum: Speed

@dataclass
class Dimension3D:
    """
    Represents the 3D dimension of an object.
    """
    length: Distance
    width: Distance
    height: Distance