"""The store commands."""

import logging

import typer

from .add_all_bases import app as add_all_bases_app
from .add_base import app as add_base_app
from .create import app as create_app
from .parse.parse import app as parse_app
from .parse.parse_all import app as parse_all_app
from .rebuild import app as rebuild_app
from .stats import app as stats_app

logger = logging.getLogger(__name__)
app = typer.Typer()
app.add_typer(create_app)
app.add_typer(add_base_app)
app.add_typer(add_all_bases_app)
app.add_typer(parse_app)
app.add_typer(parse_all_app)
app.add_typer(rebuild_app)
app.add_typer(stats_app)
