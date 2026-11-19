from client.issues_api import IssuesApi
from schemas.issue import IssueItem


def test_get_issues(issues_api: IssuesApi):
    response = issues_api.get_all(
        params={
            "fields": "id,idReadable,summary,project(name)",
            "$top": 5,
        },
    )
    issues = response.json()
    assert response.status_code == 200
    assert isinstance(issues, list)
    assert len(issues) <= 5

    for issue in issues:
        IssueItem.model_validate(issue)
