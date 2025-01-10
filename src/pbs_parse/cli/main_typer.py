"""Command-line interface."""

import logging

import typer

from .create_store import app as create_store_app
from .default_callback import base_options
from .manual import app as manual_app
from .store import app as store_app

logger = logging.getLogger(__name__)


app = typer.Typer(callback=base_options, no_args_is_help=True)


app.add_typer(store_app, name="store", help="Use a data store for the PBS data.")
app.add_typer(create_store_app, help="Create a new PBS bid period data store.")
app.add_typer(manual_app, name="manual", help="Manually execute parse commands.")


if __name__ == "__main__":
    app()
