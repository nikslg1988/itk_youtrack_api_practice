from client.issues_api import IssuesApi
from schemas.issue import Issue


def test_get_issue_by_id(
    issues_api: IssuesApi,
    created_issue: Issue,
):
    get_response = issues_api.get_by_id(
        created_issue.id,
        params={
            "fields": "id,idReadable,summary,description,project(id,name)",
        },
    )

    assert get_response.status_code == 200

    issue = Issue.model_validate(get_response.json())

    assert issue.id == created_issue.id
    assert issue.id_readable == created_issue.id_readable
    assert issue.summary == created_issue.summary
    assert issue.description == created_issue.description
    assert issue.project.id == created_issue.project.id
    assert issue.project.name == created_issue.project.name
