import toml


def get_version_from_pyproject():
    try:
        with open("pyproject.toml", "r") as f:
            pyproject_data = toml.load(f)
            return pyproject_data["tool"]["poetry"]["version"]
    except (FileNotFoundError, KeyError):
        return "unknown"


__version__ = get_version_from_pyproject()
