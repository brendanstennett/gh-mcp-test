#!/usr/bin/env python3
"""
FastAPI Application Module Entry Point

This module enables running the FastAPI CLI using the python -m syntax:
    python -m fastapi-app serve
    python -m fastapi-app status
    python -m fastapi-app db init

This provides an alternative to the direct execution methods:
    python cli.py serve
    fastapi-app serve
"""

from cli import app

if __name__ == "__main__":
    app()
