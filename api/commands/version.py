"""
Version Command Module

This module contains the version command for displaying the FastAPI application version.
"""

import typer
import tomllib
from pathlib import Path


def version():
    """
    Show the application version.

    This command displays the current version of the FastAPI application
    along with other relevant version information.
    """


    try:
        pyproject_path = Path("pyproject.toml")
        if pyproject_path.exists():
            with open(pyproject_path, "rb") as f:
                pyproject_data = tomllib.load(f)
            app_version = pyproject_data.get("project", {}).get("version", "0.1.0")
        else:
            app_version = "0.1.0"
    except Exception:
        app_version = "0.1.0"

    typer.echo(app_version)
