"""split trips cli."""

import logging

import typer

# from .all_trips import app as all_trips_app
# from .page import app as trip_app
from .split import app as split_app

logger = logging.getLogger(__name__)
app = typer.Typer()
app.add_typer(split_app)
# app.add_typer(trip_app)
# app.add_typer(all_trips_app)
