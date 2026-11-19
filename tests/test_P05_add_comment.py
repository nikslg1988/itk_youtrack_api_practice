from uuid import uuid4

from client.comments_api import CommentsApi
from schemas.issue import Issue


def test_add_comment(
    comments_api: CommentsApi,
    created_issue: Issue,
):
    test_comment = f"API comment test {uuid4()}"

    comment_fields = "id,text"

    comment_post = comments_api.create(
        created_issue.id,
        data={"text": test_comment},
        params={"fields": comment_fields},
    )

    assert comment_post.status_code == 200

    comment_get = comments_api.get_all(
        created_issue.id,
        params={"fields": comment_fields},
    )

    assert comment_get.status_code == 200

    comments = comment_get.json()

    assert any(comment["text"] == test_comment for comment in comments)
