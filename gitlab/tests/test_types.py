# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 Gauvain Pocentek <gauvain@pocentek.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gitlab import types


class TestGitlabAttribute:
    def test_all(self):
        o = types.GitlabAttribute("whatever")
        assert "whatever" == o.get()

        o.set_from_cli("whatever2")
        assert "whatever2" == o.get()

        assert "whatever2" == o.get_for_api()

        o = types.GitlabAttribute()
        assert None == o._value


class TestListAttribute:
    def test_list_input(self):
        o = types.ListAttribute()
        o.set_from_cli("foo,bar,baz")
        assert ["foo", "bar", "baz"] == o.get()

        o.set_from_cli("foo")
        assert ["foo"] == o.get()

    def test_empty_input(self):
        o = types.ListAttribute()
        o.set_from_cli("")
        assert [] == o.get()

        o.set_from_cli("  ")
        assert [] == o.get()

    def test_get_for_api_from_cli(self):
        o = types.ListAttribute()
        o.set_from_cli("foo,bar,baz")
        assert "foo,bar,baz" == o.get_for_api()

    def test_get_for_api_from_list(self):
        o = types.ListAttribute(["foo", "bar", "baz"])
        assert "foo,bar,baz" == o.get_for_api()

    def test_get_for_api_does_not_split_string(self):
        o = types.ListAttribute("foo")
        assert "foo" == o.get_for_api()


class TestLowercaseStringAttribute:
    def test_get_for_api(self):
        o = types.LowercaseStringAttribute("FOO")
        assert "foo" == o.get_for_api()
