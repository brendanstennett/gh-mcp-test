# FastAPI Application

A well-structured FastAPI application with a powerful CLI interface built using Typer.

## Features

- 🚀 FastAPI web framework with async support
- 🔧 Typer-based CLI for application management
- 🗄️ SQLModel for database operations
- 🧪 Pytest for testing
- 🔄 Hot reload in development mode
- 🏭 Production-ready server configuration

## Installation

1. Clone the repository
2. Install dependencies using uv:
   ```bash
   uv sync
   ```

## CLI Usage

The application provides a command-line interface for managing the FastAPI server and other operations.

### Available Commands

The CLI is organized into several command groups:

#### Server Management

Start the development server with hot reload:
```bash
python cli.py serve
```

Start the production server with multiple workers:
```bash
python cli.py serve --prod
```

Customize server options:
```bash
python cli.py serve --host 127.0.0.1 --port 3000
python cli.py serve --prod --workers 8 --log-level info
```

#### Application Information

Check application status:
```bash
python cli.py status
```

Show version information:
```bash
python cli.py version
```

#### Database Management

Initialize database and create tables:
```bash
python cli.py db init
```

Check database connection and status:
```bash
python cli.py db check
python cli.py db check --verbose  # Show detailed information
```

Reset database (WARNING: deletes all data):
```bash
python cli.py db reset
```

#### Help

Get help for any command:
```bash
python cli.py --help
python cli.py serve --help
python cli.py db --help
python cli.py db init --help
```

### Server Options

| Option | Description | Default | Development | Production |
|--------|-------------|---------|-------------|------------|
| `--prod` | Enable production mode | `False` | ❌ | ✅ |
| `--host` | Host to bind server to | `0.0.0.0` | ✅ | ✅ |
| `--port` | Port to bind server to | `8000` | ✅ | ✅ |
| `--workers` | Number of worker processes | `4` | ❌ | ✅ |
| `--log-level` | Log level (debug, info, warning, error) | `info`/`warning` | ✅ | ✅ |

## Development vs Production

### Development Mode (Default)
- Hot reload enabled
- Single worker process
- Detailed logging (`info` level)
- Access logs enabled
- Watches `api/` directory for changes

### Production Mode (`--prod`)
- No hot reload
- Multiple worker processes (default: 4)
- Minimal logging (`warning` level)
- Access logs disabled
- Optimized for performance

## Project Structure

```
fastapi-app/
├── api/
│   ├── boot/           # Application bootstrap
│   ├── commands/       # CLI command modules
│   ├── middleware/     # Custom middleware
│   ├── models/         # Database models
│   ├── routers/        # API route handlers
│   └── services/       # Business logic
├── migrations/         # Database migrations
├── tests/             # Test files
├── cli.py            # Main CLI entry point
├── main.py           # Legacy entry point (deprecated)
└── pyproject.toml    # Project configuration
```

## API Endpoints

Once the server is running, you can access:

- **Root**: `http://localhost:8000/` - Welcome message
- **Health Check**: `http://localhost:8000/healthz` - Health status
- **API Documentation**: `http://localhost:8000/docs` - Swagger UI
- **ReDoc**: `http://localhost:8000/redoc` - Alternative API docs

## Examples

### Quick Start Development Server
```bash
python cli.py serve
# Server starts at http://0.0.0.0:8000 with hot reload
```

### Production Deployment
```bash
python cli.py serve --prod --workers 8 --log-level warning
# Production server with 8 workers
```

### Custom Development Setup
```bash
python cli.py serve --host 127.0.0.1 --port 3000 --log-level debug
# Development server on localhost:3000 with debug logging
```

### Database Setup
```bash
# Initialize the database
python cli.py db init

# Check database status
python cli.py db check --verbose
```

## Migration from Legacy main.py

The legacy `main.py` file is deprecated in favor of the new Typer CLI. Here's the migration guide:

| Legacy Command | New CLI Command |
|----------------|-----------------|
| `python main.py` | `python cli.py serve` |
| `python main.py --prod` | `python cli.py serve --prod` |
| `python main.py --port 3000` | `python cli.py serve --port 3000` |
| `python main.py --host 127.0.0.1` | `python cli.py serve --host 127.0.0.1` |

## Contributing

1. Install development dependencies: `uv sync`
2. Initialize database: `python cli.py db init`
3. Run tests: `pytest`
4. Start development server: `python cli.py serve`
5. Check application status: `python cli.py status`

## License

This project is licensed under the MIT License.