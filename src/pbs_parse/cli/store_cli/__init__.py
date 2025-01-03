"""The store commands."""

import logging
from pathlib import Path
from typing import Annotated

import typer

from pbs_parse.pbs_2022_01.pbs_manifest.exceptions import StoreManagerException
from pbs_parse.pbs_2022_01.pbs_manifest.store_manager import StoreManager

from .add_all_bases import app as add_all_bases_app
from .add_base import app as add_base_app
from .create import app as create_app
from .parse.parse import app as parse_app
from .parse.parse_all import app as parse_all_app
from .rebuild import app as rebuild_app
from .stats import app as stats_app

logger = logging.getLogger(__name__)


def callback(
    ctx: typer.Context,
    store_directory: Annotated[
        Path,
        typer.Argument(help="Directory of the data store."),
    ],
):
    """The data store."""
    ctx.ensure_object(dict)
    try:
        store = StoreManager(manifest_directory=store_directory)
        ctx.obj["DISK_STORE"] = store
    except StoreManagerException as e:
        raise typer.BadParameter(f"Unable to load Pbs Store. error: {e}") from e


app = typer.Typer(callback=callback)
app.add_typer(create_app)
app.add_typer(add_base_app)
app.add_typer(add_all_bases_app)
app.add_typer(parse_app)
app.add_typer(parse_all_app)
app.add_typer(rebuild_app)
app.add_typer(stats_app)
