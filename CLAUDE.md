# Git Workflow

The github repository for this project is https://github.com/brendanstennett/gh-mcp-test.

This project uses gitflow for development of features. For each feature, a new branch should
be create off of the `develop` branch named `feature/<ticket_number>`. PRs should be submitted
to `develop`.

# Project Structure

## Backend (Python FastAPI)

Backend code is located in `api/` and follows this structure:

- **Routes** (`api/routers/`): Keep routes slim - they should handle request/response validation and delegate to services. Use SQLModel entities directly in route signatures.
- **Models** (`api/models/`): SQLModel entities representing database tables
- **Services** (`api/services/` and `api/services/repositories/`): Business logic and data access
- **Schemas** (`api/schemas/`): Only used for fastapi-users integration. Do NOT create separate schemas for other models - use SQLModel entities directly in routes.
- **Setup** (`api/setup/`): Application initialization (app, auth, database, dependencies)
- **Commands** (`api/commands/`): CLI commands via Typer

## Frontend (SvelteKit)

Frontend code is located in `frontend/` and is a SvelteKit application.

- API requests should be made in `PageLoad` functions to fetch data server-side
- Use the `generate-api-types` script to generate TypeScript types from the FastAPI OpenAPI spec

# Database

- **ORM**: SQLModel is the only acceptable ORM for this project
- **Migrations**: Managed via Alembic (config in `alembic.ini`, migrations in `migrations/`)
- Database setup and connection logic is in `api/setup/database.py`

# Testing

- **Framework**: Pytest
- **Location**: `tests/` directory
- **Philosophy**: Prefer using fixtures over heavy mocking, especially for database calls
- All implementations should have associated tests
- Run tests with: `python -m pytest tests/ -v`

# Code Quality

- **Formatter/Linter**: Ruff (config in `ruff.toml`)
  - Line length: 120 characters
  - Runs formatting, linting, import sorting
- **Type Checking**: basedpyright (config in `pyproject.toml`)
