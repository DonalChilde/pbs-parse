"""FILE: __init__.py."""

import typer

from .expanded_debug import app as expanded_debug_app

app = typer.Typer()

app.add_typer(expanded_debug_app)
