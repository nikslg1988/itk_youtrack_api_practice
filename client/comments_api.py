from typing import Any

import requests

from client.endpoints import YouTrackEndpoints
from client.youtrack_client import YouTrackClient


class CommentsApi:
    def __init__(self, client: YouTrackClient) -> None:
        self._client = client

    def get_all(
        self,
        issue_id: str,
        params: dict[str, Any] | None = None,
    ) -> requests.Response:
        return self._client.get(
            YouTrackEndpoints.issue_comments(issue_id),
            params=params,
        )

    def create(
        self,
        issue_id: str,
        data: dict[str, Any],
        params: dict[str, Any] | None = None,
    ) -> requests.Response:
        return self._client.post(
            YouTrackEndpoints.issue_comments(issue_id),
            json=data,
            params=params,
        )
