"""FILE: add_all.py."""

import logging
import re
from pathlib import Path
from typing import Annotated, TypedDict

import typer

from pbs_parse.pbs_2022_01.pbs_manifest.store_manager import StoreManager

logger = logging.getLogger(__name__)
app = typer.Typer()

BASE_REGEX = r"PBS_(?P<base>[A-Z]{3,3})_.*"
BASE_PATTERN = re.compile(BASE_REGEX)


class FilePair(TypedDict):
    """FilePair."""

    source_pdf: Path
    source_txt: Path
    name: str


@app.command()
def add_all_bases(
    ctx: typer.Context,
    store_directory: Annotated[
        Path,
        typer.Argument(
            help="Directory of the data store.", exists=True, file_okay=False
        ),
    ],
    path_in: Annotated[
        Path,
        typer.Argument(
            help="The directory containing bid package PDF and TXT files.",
            exists=True,
            file_okay=False,
        ),
    ],
):
    """Add all the PDF and TXT files in a directory to the store.

    Collects all the pdf files in a directory, parses out the base name, then collects
    all the TXT files with matching stem names, ie. where the name is the same but for
    the .pdf or .txt ending.

    Base name is parsed from the pdf file name in the format `PBS_PHX_*`. Files without
    a base name will be skipped.
    """
    typer.echo("Searching for pdf files...")
    glob = "*.pdf"
    file_pairs: list[FilePair] = []
    pdf_files = list(path_in.glob(glob, case_sensitive=False))
    typer.echo(f"Found {len(pdf_files)} pdf files in directory.")
    for pdf_file in pdf_files:
        base = ""
        match = BASE_PATTERN.match(pdf_file.name)
        if match is None:
            typer.echo(f"Did not find a base name in {pdf_file.name}. Skipping.")
            continue
        base = match.groupdict()["base"]
        txt_file = pdf_file.with_suffix(".txt")
        if txt_file.is_file():
            file_pairs.append(
                FilePair(source_pdf=pdf_file, source_txt=txt_file, name=base)
            )
        else:
            typer.echo(
                f"Did not find a matching .txt file for {pdf_file.name}. Skipping."
            )
    typer.echo(f"Found {len(file_pairs)} bases with matching text files.")
    for pair in file_pairs:
        with StoreManager(manifest_directory=store_directory) as store:
            typer.echo(f"Adding {pair['name']} to store.")
            store.create_base_bid(**pair)
