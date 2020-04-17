"""
GitLab API : https://docs.gitlab.com/ce/api/issues.html
"""

from httmock import HTTMock, urlmatch, response, with_httmock

from .mocks import headers
from gitlab.v4.objects import ProjectIssuesStatistics


def test_issues(gl):
    @urlmatch(scheme="http", netloc="localhost", path="/api/v4/issues", method="get")
    def resp_get_issue(url, request):
        content = '[{"name": "name", "id": 1}, ' '{"name": "other_name", "id": 2}]'
        content = content.encode("utf-8")
        return response(200, content, headers, None, 5, request)

    with HTTMock(resp_get_issue):
        data = gl.issues.list()
        assert data[1].id == 2
        assert data[1].name == "other_name"


def test_project_issues_statistics(project):
    @urlmatch(
        scheme="http",
        netloc="localhost",
        path="/api/v4/projects/1/issues_statistics",
        method="get",
    )
    def resp_get_environment(url, request):
        content = """{"statistics": {"counts": {"all": 20, "closed": 5, "opened": 15}}}""".encode(
            "utf-8"
        )
        return response(200, content, headers, None, 5, request)

    with HTTMock(resp_get_environment):
        statistics = project.issuesstatistics.get()
        assert isinstance(statistics, ProjectIssuesStatistics)
        assert statistics.statistics["counts"]["all"] == 20
