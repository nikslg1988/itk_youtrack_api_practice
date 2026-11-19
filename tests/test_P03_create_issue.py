from uuid import uuid4

from client.issues_api import IssuesApi
from schemas.issue import Issue


def test_create_issue(issues_api: IssuesApi):
    summary = f"API automation test {uuid4()}"
    # Инициализируем ID заранее, чтобы finally мог проверить, была ли создана задача
    issue_id = None

    try:
        response = issues_api.create(
            data={
                "summary": summary,
                "description": "Issue created using YouTrack REST API",
                "project": {"id": "0-0"},
            },
            params={"fields": "id,idReadable,summary,description,project(id,name)"},
        )

        assert response.status_code == 200
        issue_data = response.json()
        issue_id = issue_data["id"]
        issue = Issue.model_validate(issue_data)
        assert issue.summary == summary
        assert issue.description == "Issue created using YouTrack REST API"
        assert issue.project.id == "0-0"
        assert issue.project.name == "Demo project"

        get_test_issue = issues_api.get_by_id(
            issue_id,
            params={"fields": "id,idReadable,summary,description,project(id,name)"},
        )
        assert get_test_issue.status_code == 200

        get_issue = Issue.model_validate(get_test_issue.json())

        assert get_issue.id == issue.id
        assert get_issue.id_readable == issue.id_readable
        assert get_issue.summary == issue.summary
        assert get_issue.description == issue.description
        assert get_issue.project.id == issue.project.id
        assert get_issue.project.name == issue.project.name
    finally:
        if issue_id is not None:
            delete_response = issues_api.delete(issue_id)
            assert delete_response.status_code == 200

            deleted_issue_response = issues_api.get_by_id(issue_id)
            assert deleted_issue_response.status_code == 404
