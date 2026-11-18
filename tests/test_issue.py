from uuid import uuid4

import pytest

from client.endpoints import YouTrackEndpoints
from client.youtrack_client import YouTrackClient
from schemas.issue import Issue, IssueItem


def test_get_issues(youtrack_client: YouTrackClient):
    response = youtrack_client.get(
        YouTrackEndpoints.ISSUES,
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


def test_get_issue_by_id(youtrack_client: YouTrackClient):
    summary = f"API automation test {uuid4()}"
    # Инициализируем ID заранее, чтобы finally мог проверить, была ли создана задача
    issue_id = None

    try:
        create_response = youtrack_client.post(
            YouTrackEndpoints.ISSUES,
            json={
                "summary": summary,
                "description": "Issue created using YouTrack REST API",
                "project": {"id": "0-0"},
            },
            params={"fields": "id,idReadable,summary,description,project(id,name)"},
        )

        assert create_response.status_code == 200

        issue_data = create_response.json()
        issue_id = issue_data["id"]

        created_issue = Issue.model_validate(issue_data)

        assert created_issue.summary == summary
        assert created_issue.project.id == "0-0"

        get_response = youtrack_client.get(
            YouTrackEndpoints.issue(issue_id),
            params={
                "fields": "id,idReadable,summary,description,project(id,name)",
            },
        )

        assert get_response.status_code == 200

        issue = Issue.model_validate(get_response.json())

        assert issue.id == issue_id
        assert issue.id_readable == created_issue.id_readable
        assert issue.summary == summary
        assert issue.description == "Issue created using YouTrack REST API"
        assert issue.project.id == "0-0"
        assert issue.project.name == "Demo project"

    finally:
        if issue_id is not None:
            delete_response = youtrack_client.delete(YouTrackEndpoints.issue(issue_id))

            assert delete_response.status_code == 200

            check_deleted = youtrack_client.get(YouTrackEndpoints.issue(issue_id))

            assert check_deleted.status_code == 404


def test_create_issue(youtrack_client):
    summary = f"API automation test {uuid4()}"
    # Инициализируем ID заранее, чтобы finally мог проверить, была ли создана задача
    issue_id = None

    try:
        response = youtrack_client.post(
            YouTrackEndpoints.ISSUES,
            json={
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

        get_test_issue = youtrack_client.get(
            YouTrackEndpoints.issue(issue.id),
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
            delete_response = youtrack_client.delete(YouTrackEndpoints.issue(issue_id))
            assert delete_response.status_code == 200

            deleted_issue_response = youtrack_client.get(
                YouTrackEndpoints.issue(issue_id)
            )
            assert deleted_issue_response.status_code == 404


def test_update_issue(youtrack_client):
    summary = f"API automation test {uuid4()}"
    # Инициализируем ID заранее, чтобы finally мог проверить, была ли создана задача
    issue_id = None

    try:
        response = youtrack_client.post(
            YouTrackEndpoints.ISSUES,
            json={
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

        update_response = youtrack_client.post(
            YouTrackEndpoints.issue(issue_id),
            json={"summary": "API update test"},
            params={"fields": "id,idReadable,summary"},
        )

        assert update_response.status_code == 200

        get_response = youtrack_client.get(
            YouTrackEndpoints.issue(issue_id),
            params={"fields": "id,idReadable,summary,description,project(id,name)"},
        )

        assert get_response.status_code == 200

        updated_issue = Issue.model_validate(get_response.json())
        assert updated_issue.summary == "API update test"

    finally:
        if issue_id is not None:
            delete_response = youtrack_client.delete(YouTrackEndpoints.issue(issue_id))

            assert delete_response.status_code == 200

            check_deleted = youtrack_client.get(YouTrackEndpoints.issue(issue_id))

            assert check_deleted.status_code == 404


def test_add_comment(youtrack_client):
    test_comment = f"API comment test {uuid4()}"
    summary = f"API automation test {uuid4()}"

    response = youtrack_client.post(
        YouTrackEndpoints.ISSUES,
        json={
            "summary": summary,
            "description": "Issue created using YouTrack REST API",
            "project": {"id": "0-0"},
        },
        params={"fields": "id,idReadable,summary,description,project(id,name)"},
    )

    assert response.status_code == 200

    issue = Issue.model_validate(response.json())
    try:
        assert issue.summary == summary
        assert issue.project.id == "0-0"
        comment_post = youtrack_client.post(
            YouTrackEndpoints.issue_comments(issue.id),
            json={"text": test_comment},
            params={"fields": "id,text"},
        )
        assert comment_post.status_code == 200
        comment_get = youtrack_client.get(
            YouTrackEndpoints.issue_comments(issue.id),
            params={"fields": "id,text"},
        )
        assert comment_get.status_code == 200
        comments = comment_get.json()
        assert any(comment["text"] == test_comment for comment in comments)
    finally:
        delete_response = youtrack_client.delete(YouTrackEndpoints.issue(issue.id))
        assert delete_response.status_code == 200

        check_deleted = youtrack_client.get(YouTrackEndpoints.issue(issue.id))
        assert check_deleted.status_code == 404


def test_get_nonexistent_issue(youtrack_client):
    response = youtrack_client.get(
        YouTrackEndpoints.issue("DEMO-999999"),
    )
    assert response.status_code == 404
    error_data = response.json()

    assert error_data["error"] == "Not Found"
    assert error_data["error_description"] == ("Entity with id DEMO-999999 not found")


def test_create_issue_without_summary(youtrack_client):
    response = youtrack_client.post(
        YouTrackEndpoints.ISSUES, json={"project": {"id": "0-0"}}
    )
    assert response.status_code == 400
    error_data = response.json()
    assert error_data["error"] == "invalid_properties"

    summary_error = next(
        (
            error
            for error in error_data["error_children"]
            if error["error_field"] == "summary"
        ),
        None,
    )

    assert summary_error is not None
    assert summary_error["error_developer_message"] == ("Value for summary is required")


def test_unauthorized_request(youtrack_client):
    response = youtrack_client.get(
        YouTrackEndpoints.CURRENT_USER,
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 401

    error_data = response.json()

    assert error_data["error"] == "Unauthorized"
    assert error_data["error_description"] == "Invalid token"


@pytest.mark.parametrize(
    "project_id",
    [
        "999999-9999",
        "888888-8888",
        "777777-7777",
    ],
)
def test_create_issue_invalid_project(youtrack_client, project_id):
    response = youtrack_client.post(
        YouTrackEndpoints.ISSUES,
        json={
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


def test_add_empty_comment(youtrack_client):
    summary = f"API automation test {uuid4()}"

    response = youtrack_client.post(
        YouTrackEndpoints.ISSUES,
        json={
            "summary": summary,
            "description": "Issue created using YouTrack REST API",
            "project": {"id": "0-0"},
        },
        params={"fields": "id,idReadable,summary,description,project(id,name)"},
    )

    assert response.status_code == 200

    issue = Issue.model_validate(response.json())

    try:
        assert issue.summary == summary

        comments_before_response = youtrack_client.get(
            YouTrackEndpoints.issue_comments(issue.id),
            params={"fields": "id,text"},
        )

        assert comments_before_response.status_code == 200

        comments_before = comments_before_response.json()

        comment_response = youtrack_client.post(
            YouTrackEndpoints.issue_comments(issue.id),
            json={"text": ""},
            params={"fields": "id,text"},
        )

        assert comment_response.status_code == 400

        error_data = comment_response.json()

        assert error_data["error"] == "bad_request"
        assert error_data["error_description"] == "Comment can't be empty."

        comments_after_response = youtrack_client.get(
            YouTrackEndpoints.issue_comments(issue.id),
            params={"fields": "id,text"},
        )

        assert comments_after_response.status_code == 200

        comments_after = comments_after_response.json()

        assert len(comments_after) == len(comments_before)
        assert comments_after == comments_before

    finally:
        delete_response = youtrack_client.delete(YouTrackEndpoints.issue(issue.id))

        assert delete_response.status_code == 200

        check_deleted = youtrack_client.get(YouTrackEndpoints.issue(issue.id))

        assert check_deleted.status_code == 404
