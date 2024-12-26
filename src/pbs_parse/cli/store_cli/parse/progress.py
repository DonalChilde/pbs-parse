"""FILE: progress.py."""

from rich.progress import (
    BarColumn,
    FileSizeColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    TotalFileSizeColumn,
)

progress = Progress(
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TaskProgressColumn(),
    FileSizeColumn(),
    TotalFileSizeColumn(),
    TimeElapsedColumn(),
)
