#!/usr/bin/env python3
"""
FastAPI Application Entry Point

This module provides convenient ways to run the FastAPI application in development
and production environments.

Usage:
    python main.py              # Run development server
    python main.py --prod       # Run production server
    python main.py --help       # Show help
"""

import argparse
import uvicorn


def run_development():
    """Run the application in development mode with hot reload."""
    uvicorn.run(
        "api.setup.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["api"],
        log_level="info",
        access_log=True,
        reload_excludes=["*.pyc", "*.pyo", "__pycache__", ".git", ".pytest_cache"]
    )


def run_production():
    """Run the application in production mode."""
    uvicorn.run(
        "api.setup.app:app",
        host="0.0.0.0",
        port=8000,
        workers=4,
        log_level="warning",
        access_log=False
    )


def main():
    """Main entry point with command line argument parsing."""
    parser = argparse.ArgumentParser(
        description="FastAPI Application Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                 # Development server with hot reload
  python main.py --prod          # Production server with multiple workers
  python main.py --port 3000     # Development server on port 3000
        """
    )

    parser.add_argument(
        "--prod",
        action="store_true",
        help="Run in production mode (no reload, multiple workers)"
    )

    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to run the server on (default: 8000)"
    )

    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host to run the server on (default: 0.0.0.0)"
    )

    args = parser.parse_args()

    if args.prod:
        print(f"🏭 Starting production server on {args.host}:{args.port}")
        uvicorn.run(
            "api.setup.app:app",
            host=args.host,
            port=args.port,
            workers=4,
            log_level="warning",
            access_log=False
        )
    else:
        print(f"🚀 Starting development server on {args.host}:{args.port}")
        uvicorn.run(
            "api.setup.app:app",
            host=args.host,
            port=args.port,
            reload=True,
            reload_dirs=["api"],
            log_level="info",
            access_log=True,
            reload_excludes=["*.pyc", "*.pyo", "__pycache__", ".git", ".pytest_cache"]
        )


if __name__ == "__main__":
    main()
