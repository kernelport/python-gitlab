import pytest

import gitlab


@pytest.fixture
def gl():
    return gitlab.Gitlab(
        "http://localhost", private_token="private_token", api_version=4
    )


@pytest.fixture
def group(gl):
    return gl.groups.get(1, lazy=True)


@pytest.fixture
def project(gl):
    return gl.projects.get(1, lazy=True)
