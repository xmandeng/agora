import os

import pytest


@pytest.fixture(scope="session")
def working_dir():
    return os.getcwd()


def test_cwd_exists(working_dir):
    assert os.path.exists(working_dir)


@pytest.mark.parametrize(
    "path_fragment, expected",
    [
        ("src/agora", True),
        ("src/agora_fail", False),
    ],
)
def test_path_validation(working_dir, path_fragment, expected):
    os.chdir(f"{working_dir}/unit_tests/src/agora")

    try:
        assert (path_fragment in os.getcwd()) == expected
    finally:
        os.chdir(working_dir)
