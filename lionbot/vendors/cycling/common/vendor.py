import datetime
from lionbot.domain.cycling import dataclasses
from typing import Protocol


class Vendor(Protocol):
    """A protocol for a vendor that provides workout data."""

    def get_club(self, club_id: str) -> dataclasses.Club:
        """Get club information."""

    def get_activity(self, activity_id: str) -> dataclasses.Activity:
        """Get activity information."""

    def get_user(self, user_id: str) -> dataclasses.User:
        """Get user information."""

    def get_club_activities_for_the_day(
        self, club_id: str, day: datetime.date
    ) -> list[dataclasses.Activity]:
        """Get activities for a club for the day."""
