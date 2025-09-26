"""
Serve Command Module

This module contains the serve command for starting the FastAPI application server
in both development and production modes using Typer CLI.
"""

import typer
import uvicorn
from typing_extensions import Annotated


def serve(
    prod: Annotated[bool, typer.Option("--prod", help="Run in production mode (no reload, multiple workers)")] = False,
    host: Annotated[str, typer.Option("--host", help="Host to bind the server to")] = "127.0.0.1",
    port: Annotated[int, typer.Option("--port", help="Port to bind the server to")] = 8000,
    workers: Annotated[int, typer.Option("--workers", help="Number of worker processes (production mode only)")] = 4,
    log_level: Annotated[str | None, typer.Option("--log-level", help="Log level")] = None,
):
    """
    Start the FastAPI application server.

    By default, runs in development mode with hot reload enabled.
    Use --prod flag to run in production mode with multiple workers.
    """

    if prod:
        # Production mode configuration
        effective_log_level = log_level or "info"
        typer.echo(f"🏭 Starting production server on {host}:{port} with {workers} workers")

        uvicorn.run(
            "api.setup.app:app", host=host, port=port, workers=workers, log_level=effective_log_level, access_log=False
        )
    else:
        # Development mode configuration
        effective_log_level = log_level or "info"
        typer.echo(f"🚀 Starting development server on {host}:{port}")

        uvicorn.run(
            "api.setup.app:app",
            host=host,
            port=port,
            reload=True,
            reload_dirs=["api"],
            log_level=effective_log_level,
            access_log=True,
            reload_excludes=["*.pyc", "*.pyo", "__pycache__", ".git", ".pytest_cache"],
        )
