from client.issues_api import IssuesApi


def test_get_nonexistent_issue(issues_api: IssuesApi):
    response = issues_api.get_by_id("DEMO-999999")

    assert response.status_code == 404

    error_data = response.json()

    assert error_data["error"] == "Not Found"
    assert error_data["error_description"] == ("Entity with id DEMO-999999 not found")
