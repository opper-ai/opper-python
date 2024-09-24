import re

from opperai import __version__


def test_version():
    semver_pattern = r"^\d+\.\d+\.\d+(-[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*)?(\+[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*)?$"
    assert re.match(
        semver_pattern, __version__
    ), f"version {__version__} does not follow semver format"
