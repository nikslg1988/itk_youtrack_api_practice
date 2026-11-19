from client.issues_api import IssuesApi


def test_create_issue_without_summary(issues_api: IssuesApi):
    response = issues_api.create(
        data={"project": {"id": "0-0"}},
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
