"""FILE: progress.py."""

from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
)

progress = Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    MofNCompleteColumn(),
    BarColumn(),
    TaskProgressColumn(),
    TimeElapsedColumn(),
)
