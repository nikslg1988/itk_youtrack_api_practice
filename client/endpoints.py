class YouTrackEndpoints:
    ISSUES: str = "/api/issues"
    CURRENT_USER: str = "/api/users/me"

    @staticmethod
    def issue(issue_id: str) -> str:
        return f"/api/issues/{issue_id}"

    @staticmethod
    def issue_comments(issue_id: str) -> str:
        return f"/api/issues/{issue_id}/comments"
