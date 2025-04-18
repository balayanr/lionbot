from __future__ import annotations
import dataclasses
from typing import Literal


@dataclasses.dataclass(frozen=True)
class VendorDetails:
    """A class representing a connection between a user and a vendor."""
    vendor: str
    user_identifier: str
    profile_url: str

@dataclasses.dataclass(frozen=True)
class User:
    """A class representing a user."""
    id: str
    username: str
    name: str
    profile_picture_url: str
    total_workouts: int
    total_distance: float
    total_time: int
    vendor_details: list[VendorDetails] # [StravaID, PelotonID, etc.]

@dataclasses.dataclass(frozen=True)
class Workout:
    id: str
    external_identifier: str
    status: Literal["COMPLETE", ]

class PerformanceMetrics:
    average_power: float
    duration: int # in seconds
    is_pb: bool

    @property
    def as_work(self) -> float:
        """Calculate work done in Joules."""
        return self.average_power * self.duration

@dataclasses.dataclass(frozen=True)
class Activity:
    """A class representing a ride."""
    id: str
    external_identifier: str
    

    title: str
    instructor: str
    url: str
    duration: int

    metrics: list[PerformanceMetrics]



@dataclasses.dataclass(frozen=True)
class Club:
    """A class representing a club."""
    id: str
    external_identifier: str
    name: str
    url: str
    description: str
    logo_url: str
    users: list[User]
    activities : list[Activity]

