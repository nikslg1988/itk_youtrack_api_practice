from client.issues_api import IssuesApi
from schemas.issue import Issue


def test_update_issue(
    issues_api: IssuesApi,
    created_issue: Issue,
):
    updated_summary = "API update test"

    update_response = issues_api.update(
        created_issue.id,
        data={"summary": updated_summary},
        params={"fields": "id,idReadable,summary"},
    )

    assert update_response.status_code == 200

    get_response = issues_api.get_by_id(
        created_issue.id,
        params={
            "fields": "id,idReadable,summary,description,project(id,name)",
        },
    )

    assert get_response.status_code == 200

    updated_issue = Issue.model_validate(get_response.json())

    assert updated_issue.id == created_issue.id
    assert updated_issue.id_readable == created_issue.id_readable
    assert updated_issue.summary == updated_summary
    assert updated_issue.description == created_issue.description
    assert updated_issue.project.id == created_issue.project.id
    assert updated_issue.project.name == created_issue.project.name
