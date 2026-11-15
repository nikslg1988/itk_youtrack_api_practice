from client.youtrack_client import YouTrackClient
from schemas.user import UserMe


def test_smoke(youtrack_client: YouTrackClient) -> None:
    response = youtrack_client.get("/api/users/me", params={"fields": "id,login,name"})

    assert response.status_code == 200
    user = UserMe.model_validate(response.json())

    assert user.name
    assert user.id
    assert user.login
