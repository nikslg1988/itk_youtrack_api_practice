import pytest

from client.issues_api import IssuesApi


@pytest.mark.parametrize(
    "project_id",
    [
        "999999-9999",
        "888888-8888",
        "777777-7777",
    ],
)
def test_create_issue_invalid_project(issues_api: IssuesApi, project_id: str):
    response = issues_api.create(
        data={
            "summary": "Invalid project test",
            "project": {
                "id": project_id,
            },
        },
    )

    assert response.status_code == 400

    error_data = response.json()

    assert error_data["error_description"] == (
        f"An Project-type entity with the specified ID ({project_id}) was not found"
    )
