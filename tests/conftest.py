import os
from collections.abc import Generator
from uuid import uuid4

import pytest
from dotenv import load_dotenv

from client.comments_api import CommentsApi
from client.issues_api import IssuesApi
from client.youtrack_client import YouTrackClient
from schemas.issue import Issue
from tests.constants import ISSUE_DESCRIPTION, ISSUE_FIELDS, PROJECT_ID


@pytest.fixture(scope="session")
def youtrack_config() -> dict[str, str]:
    load_dotenv()

    base_url = os.getenv("YOUTRACK_BASE_URL")
    token = os.getenv("YOUTRACK_TOKEN")

    if not base_url or not token:
        pytest.fail("Не заданы YOUTRACK_BASE_URL или YOUTRACK_TOKEN")

    return {
        "base_url": base_url.rstrip("/"),
        "token": token,
    }


@pytest.fixture(scope="function")
def youtrack_client(youtrack_config) -> Generator[YouTrackClient]:

    client = YouTrackClient(youtrack_config["base_url"], youtrack_config["token"])

    with client:
        yield client


@pytest.fixture(scope="function")
def issues_api(youtrack_client: YouTrackClient) -> IssuesApi:
    return IssuesApi(youtrack_client)


@pytest.fixture(scope="function")
def comments_api(youtrack_client: YouTrackClient) -> CommentsApi:
    return CommentsApi(youtrack_client)


@pytest.fixture(scope="function")
def created_issue(issues_api: IssuesApi) -> Generator[Issue]:
    response = issues_api.create(
        data={
            "summary": f"API automation test {uuid4()}",
            "description": ISSUE_DESCRIPTION,
            "project": {"id": PROJECT_ID},
        },
        params={"fields": ISSUE_FIELDS},
    )

    assert response.status_code == 200

    issue_data = response.json()
    issue_id = issue_data["id"]

    try:
        yield Issue.model_validate(issue_data)
    finally:
        delete_response = issues_api.delete(issue_id)
        assert delete_response.status_code == 200

        check_deleted = issues_api.get_by_id(issue_id)
        assert check_deleted.status_code == 404
