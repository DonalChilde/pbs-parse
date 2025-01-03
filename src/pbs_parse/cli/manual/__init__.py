"""FILE: __init__.py."""

import typer

from .expand import app as expand_app
from .parse import app as parse_app
from .split_to_pages import app as split_to_pages_app
from .split_to_trips import app as split_to_trips_app
from .structure import app as structure_app
from .validate_expanded import app as validate_expanded_app
from .validate_structured import app as validate_structured_app

app = typer.Typer()
app.add_typer(split_to_pages_app)
app.add_typer(split_to_trips_app)
app.add_typer(parse_app)
app.add_typer(structure_app)
app.add_typer(validate_structured_app)
app.add_typer(expand_app)
app.add_typer(validate_expanded_app)
