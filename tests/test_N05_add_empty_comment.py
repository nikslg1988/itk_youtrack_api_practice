from client.comments_api import CommentsApi
from schemas.issue import Issue


def test_add_empty_comment(
    comments_api: CommentsApi,
    created_issue: Issue,
):
    issue_id = created_issue.id
    comment_fields = "id,text"

    comments_before_response = comments_api.get_all(
        issue_id,
        params={"fields": comment_fields},
    )

    assert comments_before_response.status_code == 200

    comments_before = comments_before_response.json()

    comment_response = comments_api.create(
        issue_id,
        data={"text": ""},
        params={"fields": comment_fields},
    )

    assert comment_response.status_code == 400

    error_data = comment_response.json()

    assert error_data["error"] == "bad_request"
    assert error_data["error_description"] == "Comment can't be empty."

    comments_after_response = comments_api.get_all(
        issue_id,
        params={"fields": comment_fields},
    )

    assert comments_after_response.status_code == 200

    comments_after = comments_after_response.json()

    assert comments_after == comments_before
