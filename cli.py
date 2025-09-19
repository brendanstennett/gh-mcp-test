#!/usr/bin/env python3
"""
FastAPI Application CLI

This module provides a command-line interface for managing the FastAPI application
using Typer for command organization and argument parsing.

Usage:
    python cli.py serve              # Start development server
    python cli.py serve --prod       # Start production server
    python cli.py version            # Show version information
    python cli.py shell              # Start interactive shell with models/repos loaded
    python cli.py --help             # Show available commands
"""

import typer

# Create the main CLI application
app = typer.Typer(
    name="fastapi-app",
    help="FastAPI Application CLI - Manage your FastAPI application",
    add_completion=False,
    rich_markup_mode="rich"
)

# Import commands from the commands package
from api.commands import serve, version, init_db, check_db, reset_db, shell

# Create database command group
db_app = typer.Typer(help="Database management commands")
_ = db_app.command("init", help="Initialize database and create tables")(init_db)
_ = db_app.command("check", help="Check database connection and status")(check_db)
_ = db_app.command("reset", help="Reset database (WARNING: deletes all data)")(reset_db)

# Register commands
_ = app.command("serve")(serve)
_ = app.command("version")(version)
_ = app.command("shell", help="Start interactive shell with models and repositories loaded")(shell)
app.add_typer(db_app, name="db")

if __name__ == "__main__":
    app()
