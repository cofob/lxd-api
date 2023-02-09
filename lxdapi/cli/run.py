"""Server launch related commands."""
import os

import alembic.config
import click
import uvicorn

from .cli import cli


@cli.command()
@click.option("--host", "-h", default="0.0.0.0", help="Host to bind to.")
@click.option("--port", "-p", default=8000, help="Port to bind to.")
@click.option("--migrate", "-m", is_flag=True, help="Run migrations before starting.")
@click.option("--reload", "-r", is_flag=True, help="Reload on code changes.")
@click.option("--debug", "-d", is_flag=True, help="Enable debug mode.")
@click.option("--workers", "-w", default=1, help="Number of workers.")
@click.option("--env", "-e", multiple=True, help="Environment variables.")
def run(host: str, port: int, migrate: bool, reload: bool, debug: bool, workers: int, env: list[str]) -> None:
    """Run the LXD API webserver."""
    if migrate:
        alembic.config.main(argv=["upgrade", "head"])  # type: ignore
    for key, value in [item.split("=") for item in env]:
        os.environ[key.upper()] = value
    uvicorn.run(
        "lxdapi:app",
        host=host,
        port=port,
        reload=reload,
        debug=debug,
        workers=workers,
        factory=True,
    )


@cli.command()
def dev() -> None:
    """Run the development server."""
    os.environ["SECRET"] = "secret"
    uvicorn.run("lxdapi:app", host="127.0.0.1", port=8000, reload=True, debug=True, workers=1, factory=True)
