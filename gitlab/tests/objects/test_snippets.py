"""
GitLab API : https://docs.gitlab.com/ce/api/project_snippets.html
             https://docs.gitlab.com/ee/api/snippets.html (todo)
"""

from httmock import HTTMock, response, urlmatch

from .mocks import headers


def test_list_project_snippets(project):
    title = "Example Snippet Title"
    visibility = "private"

    @urlmatch(
        scheme="http",
        netloc="localhost",
        path="/api/v4/projects/1/snippets",
        method="get",
    )
    def resp_list_snippet(url, request):
        content = """[{
        "title": "%s",
        "description": "More verbose snippet description",
        "file_name": "example.txt",
        "content": "source code with multiple lines",
        "visibility": "%s"}]""" % (
            title,
            visibility,
        )
        content = content.encode("utf-8")
        return response(200, content, headers, None, 25, request)

    with HTTMock(resp_list_snippet):
        snippets = project.snippets.list()
        assert len(snippets) == 1
        assert snippets[0].title == title
        assert snippets[0].visibility == visibility


def test_get_project_snippets(project):
    title = "Example Snippet Title"
    visibility = "private"

    @urlmatch(
        scheme="http",
        netloc="localhost",
        path="/api/v4/projects/1/snippets/1",
        method="get",
    )
    def resp_get_snippet(url, request):
        content = """{
        "title": "%s",
        "description": "More verbose snippet description",
        "file_name": "example.txt",
        "content": "source code with multiple lines",
        "visibility": "%s"}""" % (
            title,
            visibility,
        )
        content = content.encode("utf-8")
        return response(200, content, headers, None, 25, request)

    with HTTMock(resp_get_snippet):
        snippet = project.snippets.get(1)
        assert snippet.title == title
        assert snippet.visibility == visibility


def test_create_update_project_snippets(project):
    title = "Example Snippet Title"
    visibility = "private"

    @urlmatch(
        scheme="http",
        netloc="localhost",
        path="/api/v4/projects/1/snippets",
        method="put",
    )
    def resp_update_snippet(url, request):
        content = """{
        "title": "%s",
        "description": "More verbose snippet description",
        "file_name": "example.txt",
        "content": "source code with multiple lines",
        "visibility": "%s"}""" % (
            title,
            visibility,
        )
        content = content.encode("utf-8")
        return response(200, content, headers, None, 25, request)

    @urlmatch(
        scheme="http",
        netloc="localhost",
        path="/api/v4/projects/1/snippets",
        method="post",
    )
    def resp_create_snippet(url, request):
        content = """{
        "title": "%s",
        "description": "More verbose snippet description",
        "file_name": "example.txt",
        "content": "source code with multiple lines",
        "visibility": "%s"}""" % (
            title,
            visibility,
        )
        content = content.encode("utf-8")
        return response(200, content, headers, None, 25, request)

    with HTTMock(resp_create_snippet, resp_update_snippet):
        snippet = project.snippets.create(
            {
                "title": title,
                "file_name": title,
                "content": title,
                "visibility": visibility,
            }
        )
        assert snippet.title == title
        assert snippet.visibility == visibility
        title = "new-title"
        snippet.title = title
        snippet.save()
        assert snippet.title == title
        assert snippet.visibility == visibility
