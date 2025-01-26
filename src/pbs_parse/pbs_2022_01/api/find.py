"""FILE: find.py."""

from pathlib import Path


def source_files(dir_in: Path, glob: str = "PBS_*.txt") -> list[Path]:
    """source_files.

    Args:
        dir_in (Path): _description_
        glob (str, optional): _description_. Defaults to "PBS_*.txt".

    Returns:
        list[Path]: _description_
    """
    files = list(dir_in.glob(glob, case_sensitive=False))
    return files


def page_lines(dir_in: Path, glob: str = "page-lines_*.json") -> list[Path]:
    """page_lines.

    Args:
        dir_in (Path): _description_
        glob (str, optional): _description_. Defaults to "page-lines_*.json".

    Returns:
        list[Path]: _description_
    """
    files = list(dir_in.glob(glob, case_sensitive=False))
    return files


def trip_lines(dir_in: Path, glob: str = "trip-lines_*.json") -> list[Path]:
    """trip_lines.

    Args:
        dir_in (Path): _description_
        glob (str, optional): _description_. Defaults to "trip-lines_*.json".

    Returns:
        list[Path]: _description_
    """
    files = list(dir_in.glob(glob, case_sensitive=False))
    return files


def parsed_trips(dir_in: Path, glob: str = "parsed-trip_*.json") -> list[Path]:
    """parsed_trips.

    Args:
        dir_in (Path): _description_
        glob (str, optional): _description_. Defaults to "parsed-trip_*.json".

    Returns:
        list[Path]: _description_
    """
    files = list(dir_in.glob(glob, case_sensitive=False))
    return files


def expanded_trips(dir_in: Path, glob: str = "expanded-trip_*.json") -> list[Path]:
    """expanded_trips.

    Args:
        dir_in (Path): _description_
        glob (str, optional): _description_. Defaults to "expanded-trip_*.json".

    Returns:
        list[Path]: _description_
    """
    files = list(dir_in.glob(glob, case_sensitive=False))
    return files
