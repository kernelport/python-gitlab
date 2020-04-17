"""
GitLab API: https://docs.gitlab.com/ce/api/applications.html
"""

import json

from httmock import HTTMock, urlmatch, response  # noqa


headers = {"content-type": "application/json"}
title = "GitLab Test Instance"
description = "gitlab-test.example.com"
new_title = "new-title"
new_description = "new-description"


def test_create_application(gl):
    content = '{"name": "test_app", "redirect_uri": "http://localhost:8080", "scopes": ["api", "email"]}'
    json_content = json.loads(content)

    @urlmatch(
        scheme="http", netloc="localhost", path="/api/v4/applications", method="post",
    )
    def resp_application_create(url, request):
        headers = {"content-type": "application/json"}
        return response(200, json_content, headers, None, 5, request)

    with HTTMock(resp_application_create):
        application = gl.applications.create(
            {
                "name": "test_app",
                "redirect_uri": "http://localhost:8080",
                "scopes": ["api", "email"],
                "confidential": False,
            }
        )
        assert application.name == "test_app"
        assert application.redirect_uri == "http://localhost:8080"
        assert application.scopes == ["api", "email"]


def test_get_update_appearance(gl):
    @urlmatch(
        scheme="http",
        netloc="localhost",
        path="/api/v4/application/appearance",
        method="get",
    )
    def resp_get_appearance(url, request):
        content = """{
        "title": "%s",
        "description": "%s",
        "logo": "/uploads/-/system/appearance/logo/1/logo.png",
        "header_logo": "/uploads/-/system/appearance/header_logo/1/header.png",
        "favicon": "/uploads/-/system/appearance/favicon/1/favicon.png",
        "new_project_guidelines": "Please read the FAQs for help.",
        "header_message": "",
        "footer_message": "",
        "message_background_color": "#e75e40",
        "message_font_color": "#ffffff",
        "email_header_and_footer_enabled": false}""" % (
            title,
            description,
        )
        content = content.encode("utf-8")
        return response(200, content, headers, None, 25, request)

    @urlmatch(
        scheme="http",
        netloc="localhost",
        path="/api/v4/application/appearance",
        method="put",
    )
    def resp_update_appearance(url, request):
        content = """{
        "title": "%s",
        "description": "%s",
        "logo": "/uploads/-/system/appearance/logo/1/logo.png",
        "header_logo": "/uploads/-/system/appearance/header_logo/1/header.png",
        "favicon": "/uploads/-/system/appearance/favicon/1/favicon.png",
        "new_project_guidelines": "Please read the FAQs for help.",
        "header_message": "",
        "footer_message": "",
        "message_background_color": "#e75e40",
        "message_font_color": "#ffffff",
        "email_header_and_footer_enabled": false}""" % (
            new_title,
            new_description,
        )
        content = content.encode("utf-8")
        return response(200, content, headers, None, 25, request)

    with HTTMock(resp_get_appearance), HTTMock(resp_update_appearance):
        appearance = gl.appearance.get()
        assert appearance.title == title
        assert appearance.description == description
        appearance.title = new_title
        appearance.description = new_description
        appearance.save()
        assert appearance.title == new_title
        assert appearance.description == new_description


def test_update_application_appearance(gl):
    @urlmatch(
        scheme="http",
        netloc="localhost",
        path="/api/v4/application/appearance",
        method="put",
    )
    def resp_update_appearance(url, request):
        content = """{
        "title": "%s",
        "description": "%s",
        "logo": "/uploads/-/system/appearance/logo/1/logo.png",
        "header_logo": "/uploads/-/system/appearance/header_logo/1/header.png",
        "favicon": "/uploads/-/system/appearance/favicon/1/favicon.png",
        "new_project_guidelines": "Please read the FAQs for help.",
        "header_message": "",
        "footer_message": "",
        "message_background_color": "#e75e40",
        "message_font_color": "#ffffff",
        "email_header_and_footer_enabled": false}""" % (
            new_title,
            new_description,
        )
        content = content.encode("utf-8")
        return response(200, content, headers, None, 25, request)

    with HTTMock(resp_update_appearance):
        resp = gl.appearance.update(title=new_title, description=new_description)
