from dataclasses import dataclass
from typing import List
from ..physics.types import Distance, Angle, Duration
from ..geometry.types import Point

@dataclass
class TrajectoryPoint:
    """
    Represents a single point on a trajectory.
    """
    px: Distance
    py: Distance
    heading: Angle
    time_stamp: Duration


@dataclass
class TrajectorySetStep:
    """
    Represents a set of trajectories at a specific time step.
    """
    left: List[TrajectoryPoint]
    right: List[TrajectoryPoint]
    center: TrajectoryPoint


@dataclass
class TrafficParticipantLocation:
    """
    Represents the location of a traffic participant as a bounding box.
    """
    front_left: Point
    front_right: Point
    back_left: Point
    back_right: Point


@dataclass
class TrajectorySetStepVehicleLocation:
    """
    Represents the locations of a vehicle at a specific time step within a trajectory set.
    """
    left: TrafficParticipantLocation
    right: TrafficParticipantLocation
    center: TrafficParticipantLocation


UnstructuredTrajectorySet = List[TrajectorySetStep]