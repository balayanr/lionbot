import os
import datetime
import requests
from lionbot.domain.cycling import dataclasses as core_dataclasses
from lionbot.vendors.cycling.peloton import dataclasses

from . import _queries


class _PelotonAPISession(requests.Session):
    """A custom session that automatically handles authentication."""

    username_or_email: str
    password: str

    rest_api = "https://api.onepeloton.com/"
    graphql_url = "https://gql-graphql-gateway.prod.k8s.onepeloton.com/graphql"

    def __init__(self, username_or_email: str, password: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.username_or_email = username_or_email
        self.password = password
        self._login()

    def _login(self) -> requests.Response:
        """Login to Peloton."""
        payload = {
            "username_or_email": self.username_or_email,
            "password": self.password,
        }

        return self.post("https://api.onepeloton.com/auth/login", json=payload)

    def request(self, *args, headers: dict | None = None, **kwargs):
        """Override the request method to handle 401 errors."""
        if not headers:
            headers = {
                "Content-Type": "application/json",
                "Peloton-Platform": "home_bike",
            }

        response = super().request(*args, headers=headers, **kwargs)
        if response.status_code == 401:
            # Re-login if the session is unauthorized
            self._login()
            # Retry the request after re-login
            response = super().request(*args, headers=headers, **kwargs)
        # TODO: handle other status codes
        return response

    def graphql_request(
        self, operation_name: str, query: str, variables: dict = None
    ) -> requests.Response:
        """Make a GraphQL request."""
        payload = {
            "operationName": operation_name,
            "query": query,
            "variables": variables or {},
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        return self.post(self.graphql_url, json=payload, headers=headers)


class PelotonClient:
    API: requests.Session

    def __init__(self) -> None:
        self.API = _PelotonAPISession(
            username_or_email=os.environ.get("PELOTON_USERNAME"),
            password=os.environ.get("PELOTON_PASSWORD"),
        )

    # Peloton-specific API methods
    def get_workouts(self, user_id: str) -> list[dataclasses.Workout]:
        request_url = f"api/user/{user_id}/workouts?joins=ride,ride.instructor"
        response = self.API.get(request_url)
        raw_workouts = response.json()["data"]
        return [dataclasses.Workout.from_json(workout) for workout in raw_workouts]

    def get_users_in_tag(self, tag, after: str | None = None):
        variables = {"tag": tag}
        if after:
            variables["after"] = after

        return self.API.graphql_request(
            operation_name="TagDetail",
            query=_queries.TagDetail,
            variables=variables,
        )

    # Core Vendor API methods
    def get_club(self, club_id: str) -> core_dataclasses.Club:
        """Get club information."""
        pass

    def get_activity(self, activity_id: str) -> core_dataclasses.Activity:
        """Get activity information."""
        pass

    def get_user(self, user_id: str) -> core_dataclasses.User:
        """Get user information."""
        pass

    def get_club_activities_for_the_day(
        self, club_id: str, day: datetime.date
    ) -> list[core_dataclasses.Activity]:
        """Get activities for a club for the day."""
        pass
