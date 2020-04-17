"""
GitLab API : https://docs.gitlab.com/ce/api/users.html
"""

from httmock import response, urlmatch, with_httmock
import pytest

from gitlab.v4.objects import User, UserMembership, UserStatus


@urlmatch(scheme="http", netloc="localhost", path="/api/v4/users/1", method="get")
def resp_get_user(url, request):
    headers = {"content-type": "application/json"}
    content = (
        '{"name": "name", "id": 1, "password": "password", '
        '"username": "username", "email": "email"}'
    )
    content = content.encode("utf-8")
    return response(200, content, headers, None, 5, request)


@urlmatch(
    scheme="http", netloc="localhost", path="/api/v4/users/1/memberships", method="get",
)
def resp_get_user_memberships(url, request):
    headers = {"content-type": "application/json"}
    content = """[
                  {
                    "source_id": 1,
                    "source_name": "Project one",
                    "source_type": "Project",
                    "access_level": "20"
                  },
                  {
                    "source_id": 3,
                    "source_name": "Group three",
                    "source_type": "Namespace",
                    "access_level": "20"
                  }
                ]"""
    content = content.encode("utf-8")
    return response(200, content, headers, None, 5, request)


@with_httmock(resp_get_user)
def test_get_user(gl):
    user = gl.users.get(1)
    assert isinstance(user, User)
    assert user.name == "name"
    assert user.id == 1


@with_httmock(resp_get_user_memberships)
def test_user_memberships(gl):
    user = gl.users.get(1, lazy=True)
    memberships = user.memberships.list()
    assert isinstance(memberships[0], UserMembership)
    assert memberships[0].source_type == "Project"


@urlmatch(
    scheme="http", netloc="localhost", path="/api/v4/users/1/status", method="get",
)
def resp_get_user_status(url, request):
    headers = {"content-type": "application/json"}
    content = (
        '{"message": "test", "message_html": "<h1>Message</h1>", "emoji": "thumbsup"}'
    )
    content = content.encode("utf-8")
    return response(200, content, headers, None, 5, request)


@pytest.mark.skip
@with_httmock(resp_get_user, resp_get_user_status)
def test_user_status(gl):
    user = gl.users.get(1)
    status = user.status.get()
    assert isinstance(status, UserStatus)
    assert status.message == "test"
    assert status.emoji == "thumbsup"


@urlmatch(
    scheme="http", netloc="localhost", path="/api/v4/users/1/activate", method="post",
)
def resp_activate(url, request):
    headers = {"content-type": "application/json"}
    return response(201, {}, headers, None, 5, request)


@urlmatch(
    scheme="http", netloc="localhost", path="/api/v4/users/1/deactivate", method="post",
)
def resp_deactivate(url, request):
    headers = {"content-type": "application/json"}
    return response(201, {}, headers, None, 5, request)


@with_httmock(resp_activate, resp_deactivate)
def test_user_activate_deactivate(gl):
    gl.users.get(1, lazy=True).activate()
    gl.users.get(1, lazy=True).deactivate()
