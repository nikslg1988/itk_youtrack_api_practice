import os
from collections.abc import Generator

import pytest
from dotenv import load_dotenv

from client.youtrack_client import YouTrackClient


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
