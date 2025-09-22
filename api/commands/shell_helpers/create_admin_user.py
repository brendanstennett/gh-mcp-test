"""
Admin User Creation Helper

Provides functionality to create admin users with superuser privileges.
"""

import asyncio
from rich.console import Console

from api.models.user import User
from api.setup.database import async_session_maker
from api.setup.auth import get_user_db, get_user_manager

console = Console()

async def create_admin_user(email: str, password: str, session = None):
    """
    Create an admin user with superuser privileges.

    Args:
        email: User's email address
        password: User's password (will be hashed)
        session: Optional database session (uses default if not provided)

    Returns:
        User: The created admin user
    """
    if session is None:
        session = async_session_maker()
        close_session = True
    else:
        close_session = False

    try:
        user_db_gen = get_user_db(session)
        user_db = await user_db_gen.__anext__()

        user_manager_gen = get_user_manager(user_db)
        user_manager = await user_manager_gen.__anext__()

        # Create user with admin privileges
        from api.schemas.user import UserCreate

        # Create user data schema
        user_create = UserCreate(
            email=email,
            password=password,
            is_active=True,
            is_superuser=True,
            is_verified=True
        )

        user = await user_manager.create(user_create)

        console.print(f"[bold green]Admin user created successfully![/bold green]")
        console.print(f"Email: {user.email}")
        console.print(f"ID: {user.id}")
        console.print(f"Is superuser: {user.is_superuser}")

        return user

    except Exception as e:
        console.print(f"[bold red]Error creating admin user: {e}[/bold red]")
        raise
    finally:
        if close_session:
            await session.close()