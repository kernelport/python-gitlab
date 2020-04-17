# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Mika Mäenpää <mika.j.maenpaa@tut.fi>,
#                    Tampere University of Technology
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or`
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import pickle
import tempfile

from httmock import HTTMock  # noqa
from httmock import response  # noqa
from httmock import urlmatch  # noqa

import gitlab
from gitlab import *  # noqa
from gitlab.v4.objects import *  # noqa
import pytest


valid_config = b"""[global]
default = one
ssl_verify = true
timeout = 2

[one]
url = http://one.url
private_token = ABCDEF
"""


class TestGitlabList:
    def test_build_list(self, gl):
        @urlmatch(scheme="http", netloc="localhost", path="/api/v4/tests", method="get")
        def resp_1(url, request):
            headers = {
                "content-type": "application/json",
                "X-Page": 1,
                "X-Next-Page": 2,
                "X-Per-Page": 1,
                "X-Total-Pages": 2,
                "X-Total": 2,
                "Link": (
                    "<http://localhost/api/v4/tests?per_page=1&page=2>;" ' rel="next"'
                ),
            }
            content = '[{"a": "b"}]'
            return response(200, content, headers, None, 5, request)

        @urlmatch(
            scheme="http",
            netloc="localhost",
            path="/api/v4/tests",
            method="get",
            query=r".*page=2",
        )
        def resp_2(url, request):
            headers = {
                "content-type": "application/json",
                "X-Page": 2,
                "X-Next-Page": 2,
                "X-Per-Page": 1,
                "X-Total-Pages": 2,
                "X-Total": 2,
            }
            content = '[{"c": "d"}]'
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_1):
            obj = gl.http_list("/tests", as_list=False)
            assert len(obj) == 2
            assert obj._next_url == "http://localhost/api/v4/tests?per_page=1&page=2"
            assert obj.current_page == 1
            assert obj.prev_page == None
            assert obj.next_page == 2
            assert obj.per_page == 1
            assert obj.total_pages == 2
            assert obj.total == 2

            with HTTMock(resp_2):
                l = list(obj)
                assert len(l) == 2
                assert l[0]["a"] == "b"
                assert l[1]["c"] == "d"

    def test_all_omitted_when_as_list(self, gl):
        @urlmatch(scheme="http", netloc="localhost", path="/api/v4/tests", method="get")
        def resp(url, request):
            headers = {
                "content-type": "application/json",
                "X-Page": 2,
                "X-Next-Page": 2,
                "X-Per-Page": 1,
                "X-Total-Pages": 2,
                "X-Total": 2,
            }
            content = '[{"c": "d"}]'
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp):
            result = gl.http_list("/tests", as_list=False, all=True)
            assert isinstance(result, GitlabList)


@pytest.fixture
def gl_trailing():
    return gitlab.Gitlab(
        "http://localhost", private_token="private_token", api_version=4
    )


class TestGitlabStripBaseUrl:
    def test_strip_base_url(self, gl_trailing):
        assert gl_trailing.url == "http://localhost"

    def test_strip_api_url(self, gl_trailing):
        assert gl_trailing.api_url == "http://localhost/api/v4"

    def test_build_url(self, gl_trailing):
        r = gl_trailing._build_url("/projects")
        assert r == "http://localhost/api/v4/projects"


class TestGitlab:
    def test_pickability(self, gl):
        original_gl_objects = gl._objects
        pickled = pickle.dumps(gl)
        unpickled = pickle.loads(pickled)
        assert isinstance(unpickled, Gitlab)
        assert hasattr(unpickled, "_objects")
        assert unpickled._objects == original_gl_objects

    def test_token_auth(self, gl, callback=None):
        name = "username"
        id_ = 1

        @urlmatch(scheme="http", netloc="localhost", path="/api/v4/user", method="get")
        def resp_cont(url, request):
            headers = {"content-type": "application/json"}
            content = '{{"id": {0:d}, "username": "{1:s}"}}'.format(id_, name).encode(
                "utf-8"
            )
            return response(200, content, headers, None, 5, request)

        with HTTMock(resp_cont):
            gl.auth()
        assert gl.user.username == name
        assert gl.user.id == id_
        assert isinstance(gl.user, CurrentUser)

    def _default_config(self):
        fd, temp_path = tempfile.mkstemp()
        os.write(fd, valid_config)
        os.close(fd)
        return temp_path

    def test_from_config(self):
        config_path = self._default_config()
        gitlab.Gitlab.from_config("one", [config_path])
        os.unlink(config_path)

    def test_subclass_from_config(self, gl):
        class MyGitlab(gitlab.Gitlab):
            pass

        config_path = self._default_config()
        gl = MyGitlab.from_config("one", [config_path])
        assert isinstance(gl, MyGitlab)
        os.unlink(config_path)
