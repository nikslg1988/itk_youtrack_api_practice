from client.endpoints import YouTrackEndpoints


def test_unauthorized_request(youtrack_client):
    response = youtrack_client.get(
        YouTrackEndpoints.CURRENT_USER,
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 401

    error_data = response.json()

    assert error_data["error"] == "Unauthorized"
    assert error_data["error_description"] == "Invalid token"
