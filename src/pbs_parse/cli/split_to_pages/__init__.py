"""split pages cli."""

import logging

import typer

from .all_pages import app as all_pages_app
from .page import app as page_app

logger = logging.getLogger(__name__)
app = typer.Typer()
app.add_typer(page_app)
app.add_typer(all_pages_app)
