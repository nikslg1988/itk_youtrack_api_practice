from types import TracebackType
from typing import Any

import requests


class YouTrackClient:
    def __init__(self, base_url: str, api_token: str, timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.api_token = api_token
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Authorization": f"Bearer {self.api_token}",
            }
        )

    def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> requests.Response:

        return self._request("GET", endpoint, params=params, headers=headers)

    def post(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> requests.Response:

        return self._request(
            "POST", endpoint, params=params, json=json, headers=headers
        )

    def delete(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> requests.Response:

        return self._request("DELETE", endpoint, params=params, headers=headers)

    def _request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> requests.Response:

        url = self.base_url + "/" + endpoint.lstrip("/")
        response = self.session.request(
            method,
            url,
            params=params,
            json=json,
            headers=headers,
            timeout=self.timeout,
        )
        return response

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ):
        self.session.close()
        return False
