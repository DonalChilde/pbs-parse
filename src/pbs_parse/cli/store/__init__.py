"""FILE: __init__.py."""

from pathlib import Path
from typing import Annotated, TypedDict

import typer

from pbs_parse.pbs_2022_01.pbs_manifest.exceptions import StoreManagerException
from pbs_parse.pbs_2022_01.pbs_manifest.store_manager import StoreManager

from .add_all_bases import app as add_all_bases_app
from .add_base import app as add_base_app
from .do import app as do_app
from .export import app as export_app
from .stats import app as stats_app


class StoreData(TypedDict):
    """StoreData."""

    store_dir: Path
    store: StoreManager


def callback(
    ctx: typer.Context,
    store_directory: Annotated[
        Path,
        typer.Option(help="Directory of the data store.", exists=True, file_okay=False),
    ],
):
    """The data store."""
    ctx.ensure_object(dict)
    try:
        store = StoreManager(manifest_directory=store_directory)
        store_data = StoreData(store_dir=store_directory, store=store)
        ctx.obj["store_data"] = store_data
    except StoreManagerException as e:
        raise typer.BadParameter(f"Unable to load Pbs Store. error: {e}") from e


# app = typer.Typer(callback=callback)

app = typer.Typer()

# app_store = typer.Typer()
# app.add_typer(app_store)


# @app_store.command()
# def store(
#     ctx: typer.Context,
#     store_directory: Annotated[
#         Path,
#         typer.Argument(help="Directory of the data store."),
#     ],
# ):
#     """The data store."""
#     ctx.ensure_object(dict)
#     try:
#         store = StoreManager(manifest_directory=store_directory)
#         store_data = StoreData(store_dir=store_directory, store=store)
#         ctx.obj["store_data"] = store_data
#     except StoreManagerException as e:
#         raise typer.BadParameter(f"Unable to load Pbs Store. error: {e}") from e


# app_store.add_typer(do_app)
# app_store.add_typer(add_base_app)
# app_store.add_typer(add_all_bases_app)
# app_store.add_typer(stats_app)

app.add_typer(do_app)
app.add_typer(add_base_app)
app.add_typer(add_all_bases_app)
app.add_typer(stats_app)
app.add_typer(export_app, name="export", help="Export data from store.")
