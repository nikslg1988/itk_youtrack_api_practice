from typing import Any

import requests

from client.endpoints import YouTrackEndpoints
from client.youtrack_client import YouTrackClient


class IssuesApi:
    def __init__(self, client: YouTrackClient) -> None:
        self._client = client

    def get_all(self, params: dict[str, Any] | None = None) -> requests.Response:

        return self._client.get(
            YouTrackEndpoints.ISSUES,
            params=params,
        )

    def get_by_id(
        self, issue_id: str, params: dict[str, Any] | None = None
    ) -> requests.Response:

        return self._client.get(
            YouTrackEndpoints.issue(issue_id),
            params=params,
        )

    def create(
        self,
        data: dict[str, Any],
        params: dict[str, Any] | None = None,
    ) -> requests.Response:

        return self._client.post(
            YouTrackEndpoints.ISSUES,
            json=data,
            params=params,
        )

    def update(
        self,
        issue_id: str,
        data: dict[str, Any],
        params: dict[str, Any] | None = None,
    ) -> requests.Response:

        return self._client.post(
            YouTrackEndpoints.issue(issue_id), json=data, params=params
        )

    def delete(
        self,
        issue_id: str,
        params: dict[str, Any] | None = None,
    ) -> requests.Response:

        return self._client.delete(
            YouTrackEndpoints.issue(issue_id),
            params=params,
        )
