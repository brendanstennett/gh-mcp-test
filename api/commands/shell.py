#!/usr/bin/env python3
"""
Interactive Shell Command

Starts a Python REPL with models and repositories pre-loaded for easy interaction.
"""

import asyncio
import code
from typing import Any

from sqlmodel import SQLModel

try:
    from IPython import start_ipython  # pyright: ignore[reportUnknownVariableType]

    has_ipython = True
except ImportError:
    start_ipython = None
    has_ipython = False

from rich.console import Console
from rich.table import Table

from api.commands.shell_helpers.create_admin_user import create_admin_user
from api.models.post import Post
from api.models.user import User
from api.services.repositories.posts_repository import PostsRepository
from api.setup.database import async_session_maker, engine

console = Console()


def shell():
    """Start an interactive Python shell with models and repositories pre-loaded."""

    async def setup_session():
        return async_session_maker()

    session = asyncio.run(setup_session())

    models: dict[str, type[SQLModel]] = {"Post": Post, "User": User}

    repos = {
        "posts_repository": PostsRepository(session),
    }

    database_utils: dict[str, Any] = {
        "engine": engine,
        "session": session,
        "async_session_maker": async_session_maker,
    }

    utilities = {
        "asyncio": asyncio,
    }

    helpers = {
        "create_admin_user": create_admin_user,
    }

    # Pre-loaded variables for the shell
    shell_locals: dict[str, Any] = {**models, **repos, **database_utils, **utilities, **helpers}

    # Display welcome banner
    banner_table = Table(title="FastAPI App Interactive Shell", show_header=False)
    banner_table.add_column("Item", style="bold blue")
    banner_table.add_column("Description", style="dim")

    banner_table.add_row("Models", ", ".join(models.keys()))
    banner_table.add_row("Repositories", ", ".join(repos.keys()))
    banner_table.add_row("Database", ", ".join(database_utils.keys()))
    banner_table.add_row("Utilities", ", ".join(utilities.keys()))
    banner_table.add_row("Helpers", ", ".join(helpers.keys()))

    console.print("\n")
    console.print(banner_table)
    console.print("\n[bold yellow]Example usage:[/bold yellow]")
    console.print("  [green]post = Post(title='Hello', body='World', is_published=True)[/green]")
    if has_ipython:
        console.print("  [green]await posts_repository.create_post(post)[/green]")
        console.print("  [green]await create_admin_user('admin@example.com', 'password123')[/green]")
    else:
        console.print("  [green]created = asyncio.run(posts_repository.create_post(post))[/green]")
        console.print("  [green]admin = asyncio.run(create_admin_user('admin@example.com', 'password123'))[/green]")
    console.print("  [dim]# Session will be automatically closed on exit[/dim]")
    console.print("\n")

    # Start the interactive console
    try:
        console.print("[bold green]Starting interactive shell...[/bold green]")
        if has_ipython and start_ipython is not None:
            start_ipython(argv=[], user_ns=shell_locals)
        else:
            console.print("[yellow]Note: Install IPython for better async support: pip install ipython[/yellow]")
            code.interact(banner="", local=shell_locals, exitmsg="[bold red]Exiting shell...[/bold red]")
    finally:
        asyncio.run(session.close())
        console.print("[bold green]Session closed.[/bold green]")
