"""split pages cli."""

import logging

import typer

# from .all_packages import app as all_pages_app
# from .package import app as page_app
from .split import app as split_app

logger = logging.getLogger(__name__)
app = typer.Typer()
app.add_typer(split_app)
# app.add_typer(page_app)
# app.add_typer(all_pages_app)
