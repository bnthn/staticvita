try:
    from importlib.metadata import PackageNotFoundError, version

    __version__ = version("jinja-cv")
except PackageNotFoundError:  # pragma: no cover - editable tree without install
    __version__ = "0.0.0"
