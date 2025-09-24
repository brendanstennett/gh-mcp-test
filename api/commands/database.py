"""
Database Command Module

This module contains database-related commands for the FastAPI application,
including database initialization, migration, and maintenance operations.
"""

import asyncio
import typer
from typing_extensions import Annotated
from api.setup.database import create_db_and_tables, engine
from sqlmodel import text


def database():
    """
    Database management commands.

    This is a placeholder for the database command group. Individual
    database operations should be implemented as separate functions.
    """
    pass


def init_db(
    force: Annotated[
        bool,
        typer.Option(
            "--force",
            help="Force recreate all tables (WARNING: This will delete existing data)",
        ),
    ] = False,
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Show detailed output")] = False,
):
    """
    Initialize the database and create all tables.

    This command creates all database tables defined in the SQLModel models.
    Use --force to recreate tables (this will delete existing data).
    """

    if force:
        typer.echo("⚠️  WARNING: Force mode will delete all existing data!")
        if not typer.confirm("Are you sure you want to continue?"):
            typer.echo("❌ Database initialization cancelled.")
            raise typer.Abort()

    try:
        if verbose:
            typer.echo("🔄 Initializing database...")

        asyncio.run(create_db_and_tables())

        typer.echo("✅ Database initialized successfully!")

        if verbose:

            async def show_table_info():
                async with engine.begin() as conn:
                    result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
                    tables = [row[0] for row in result.fetchall()]

                    if tables:
                        typer.echo(f"📊 Created tables: {', '.join(tables)}")
                    else:
                        typer.echo("📊 No tables found (this might be normal for an empty schema)")

            asyncio.run(show_table_info())

    except Exception as e:
        typer.echo(f"❌ Database initialization failed: {str(e)}")
        raise typer.Exit(1)


def check_db(
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Show detailed database information")] = False,
):
    """
    Check database connection and show basic information.

    This command verifies that the database is accessible and optionally
    shows detailed information about the database structure.
    """

    async def check_db_async():
        async with engine.begin() as conn:
            # Test basic connectivity
            await conn.execute(text("SELECT 1"))
            typer.echo("✅ Database connection: OK")

            if verbose:
                # Get table information
                result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
                tables = [row[0] for row in result.fetchall()]

                if tables:
                    typer.echo(f"📊 Tables found: {len(tables)}")
                    for table in tables:
                        typer.echo(f"  - {table}")

                    # Get row counts for each table
                    typer.echo("\n📈 Row counts:")
                    for table in tables:
                        try:
                            count_result = await conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                            count = count_result.scalar()
                            typer.echo(f"  - {table}: {count} rows")
                        except Exception:
                            typer.echo(f"  - {table}: Unable to count rows")
                else:
                    typer.echo("📊 No tables found")

                # Database file info
                db_info_result = await conn.execute(text("PRAGMA database_list"))
                db_info = db_info_result.fetchall()
                for db in db_info:
                    if db[1] == "main":  # Main database
                        typer.echo(f"🗄️  Database file: {db[2]}")
                        break

    try:
        asyncio.run(check_db_async())

    except Exception as e:
        typer.echo(f"❌ Database connection failed: {str(e)}")
        raise typer.Exit(1)


def reset_db():
    """
    Reset the database by dropping and recreating all tables.

    WARNING: This command will delete all existing data in the database.
    """

    typer.echo("⚠️  WARNING: This will delete ALL data in the database!")
    typer.echo("This action cannot be undone.")

    if not typer.confirm("Are you sure you want to reset the database?"):
        typer.echo("❌ Database reset cancelled.")
        raise typer.Abort()

    # Double confirmation for safety
    if not typer.confirm("Type 'yes' to confirm you want to DELETE ALL DATA"):
        typer.echo("❌ Database reset cancelled.")
        raise typer.Abort()

    try:
        typer.echo("🔄 Resetting database...")

        # Drop all tables by recreating the database
        asyncio.run(create_db_and_tables())

        typer.echo("✅ Database reset completed successfully!")
        typer.echo("🔄 All tables have been recreated.")

    except Exception as e:
        typer.echo(f"❌ Database reset failed: {str(e)}")
        raise typer.Exit(1)
