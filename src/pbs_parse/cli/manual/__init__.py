"""FILE: __init__.py."""

import typer

from .expand import app as expand_app
from .parse import app as parse_app
from .split_to_pages import app as split_to_pages_app
from .split_to_trips import app as split_to_trips_app

app = typer.Typer()
app.add_typer(split_to_pages_app)
app.add_typer(split_to_trips_app)
app.add_typer(parse_app)
app.add_typer(expand_app)
