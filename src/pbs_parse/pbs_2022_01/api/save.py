"""FILE: save.py."""

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any

import yaml

from pbs_parse.pbs_2022_01.api.common import DataType
from pbs_parse.pbs_2022_01.models.expanded import ExpandedTrip
from pbs_parse.pbs_2022_01.models.page_lines import PageLines
from pbs_parse.pbs_2022_01.models.parsed_trip import ParsedTrip
from pbs_parse.pbs_2022_01.models.trip_lines import TripLines
from pbs_parse.snippets.file.check_file import check_file

from . import style


def page_lines(
    dir_out: Path,
    page_lines: PageLines,
    file_name: str = "",
    data_type: DataType = DataType.JSON,
    overwrite: bool = False,
) -> Path:
    """page_lines.

    Args:
        dir_out (Path): _description_
        page_lines (PageLines): _description_
        file_name (str, optional): _description_. Defaults to "".
        data_type (DataType, optional): _description_. Defaults to DataType.JSON.
        overwrite (bool, optional): _description_. Defaults to False.

    Returns:
        Path: _description_
    """
    match data_type:
        case DataType.JSON:
            if not file_name:
                file_name = page_lines.default_file_name()
            file_out = dir_out / file_name
            check_file(path_out=file_out, overwrite=overwrite)
            data = page_lines.model_dump_json(indent=1)
            file_out.write_text(data=data, encoding="utf-8")
            return file_out
        case DataType.YAML:
            if not file_name:
                file_name = page_lines.default_file_name()
            file_out = dir_out / file_name
            file_out = file_out.with_suffix(".yaml")
            check_file(path_out=file_out, overwrite=overwrite)
            data = page_lines.model_dump(mode="json")
            with open(file_out, mode="w", encoding="utf-8") as fp:
                yaml.dump(data, fp, indent=1)
            return file_out
        case DataType.TXT:
            if not file_name:
                file_name = page_lines.default_file_name()
            file_out = dir_out / file_name
            file_out = file_out.with_suffix(".txt")
            check_file(path_out=file_out, overwrite=overwrite, ensure_parents=True)
            file_out.write_text(str(page_lines))
            return file_out


def trip_lines(
    dir_out: Path,
    trip_lines: TripLines,
    file_name: str = "",
    data_type: DataType = DataType.JSON,
    overwrite: bool = False,
) -> Path:
    """trip_lines.

    Args:
        dir_out (Path): _description_
        trip_lines (TripLines): _description_
        file_name (str, optional): _description_. Defaults to "".
        data_type (DataType, optional): _description_. Defaults to DataType.JSON.
        overwrite (bool, optional): _description_. Defaults to False.

    Returns:
        Path: _description_
    """
    match data_type:
        case DataType.JSON:
            if not file_name:
                file_name = trip_lines.default_file_name()
            file_out = dir_out / file_name
            check_file(path_out=file_out, overwrite=overwrite)
            data = trip_lines.model_dump_json(indent=1)
            file_out.write_text(data=data, encoding="utf-8")
            return file_out
        case DataType.YAML:
            if not file_name:
                file_name = trip_lines.default_file_name()
            file_out = dir_out / file_name
            file_out = file_out.with_suffix(".yaml")
            check_file(path_out=file_out, overwrite=overwrite)
            data = trip_lines.model_dump(mode="json")
            with open(file_out, mode="w", encoding="utf-8") as fp:
                yaml.dump(data, fp, indent=1)
            return file_out
        case DataType.TXT:
            if not file_name:
                file_name = trip_lines.default_file_name()
            file_out = dir_out / file_name
            file_out = file_out.with_suffix(".txt")
            check_file(path_out=file_out, overwrite=overwrite, ensure_parents=True)
            file_out.write_text(str(trip_lines))
            return file_out


def parsed_trip(
    dir_out: Path,
    parsed_trip: ParsedTrip,
    file_name: str = "",
    data_type: DataType = DataType.JSON,
    overwrite: bool = False,
) -> Path:
    """parsed_trip.

    Args:
        dir_out (Path): _description_
        parsed_trip (ParsedTrip): _description_
        file_name (str, optional): _description_. Defaults to "".
        data_type (DataType, optional): _description_. Defaults to DataType.JSON.
        overwrite (bool, optional): _description_. Defaults to False.

    Returns:
        Path: _description_
    """
    match data_type:
        case DataType.JSON:
            if not file_name:
                file_name = parsed_trip.default_file_name()
            file_out = dir_out / file_name
            check_file(path_out=file_out, overwrite=overwrite)
            data = parsed_trip.model_dump_json(indent=1)
            file_out.write_text(data=data, encoding="utf-8")
            return file_out
        case DataType.YAML:
            if not file_name:
                file_name = parsed_trip.default_file_name()
            file_out = dir_out / file_name
            file_out = file_out.with_suffix(".yaml")
            check_file(path_out=file_out, overwrite=overwrite)
            data = parsed_trip.model_dump(mode="json")
            with open(file_out, mode="w", encoding="utf-8") as fp:
                yaml.dump(data, fp, indent=1)
            return file_out
        case DataType.TXT:
            if not file_name:
                file_name = parsed_trip.default_file_name()
            file_out = dir_out / file_name
            file_out = file_out.with_suffix(".txt")
            check_file(path_out=file_out, overwrite=overwrite, ensure_parents=True)
            file_out.write_text(str(parsed_trip))
            return file_out


def expanded_trip(
    dir_out: Path,
    expanded_trip: ExpandedTrip,
    file_name: str = "",
    data_type: DataType = DataType.JSON,
    overwrite: bool = False,
) -> Path:
    """expanded_trip.

    Args:
        dir_out (Path): _description_
        expanded_trip (ExpandedTrip): _description_
        file_name (str, optional): _description_. Defaults to "".
        data_type (DataType, optional): _description_. Defaults to DataType.JSON.
        overwrite (bool, optional): _description_. Defaults to False.

    Returns:
        Path: _description_
    """
    match data_type:
        case DataType.JSON:
            if not file_name:
                file_name = expanded_trip.default_file_name()
            file_out = dir_out / file_name
            check_file(path_out=file_out, overwrite=overwrite)
            data = expanded_trip.model_dump_json(indent=1)
            file_out.write_text(data=data, encoding="utf-8")
            return file_out
        case DataType.YAML:
            if not file_name:
                file_name = expanded_trip.default_file_name()
            file_out = dir_out / file_name
            file_out = file_out.with_suffix(".yaml")
            check_file(path_out=file_out, overwrite=overwrite)
            data = expanded_trip.model_dump(mode="json")
            with open(file_out, mode="w", encoding="utf-8") as fp:
                yaml.dump(data, fp, indent=1)
            return file_out
        case DataType.TXT:
            if not file_name:
                file_name = expanded_trip.default_file_name()
            file_out = dir_out / file_name
            file_out = file_out.with_suffix(".txt")
            check_file(path_out=file_out, overwrite=overwrite, ensure_parents=True)
            file_out.write_text(str(expanded_trip))
            return file_out


def expanded_debug(dir_out: Path, parsed: ParsedTrip, expanded: ExpandedTrip) -> Path:
    """expanded_debug.

    Args:
        dir_out (Path): _description_
        parsed (ParsedTrip): _description_
        expanded (ExpandedTrip): _description_

    Returns:
        Path: _description_
    """
    file_out = dir_out / expanded.default_file_name()
    json_out = file_out.with_name(f"{file_out.stem}_debug.json")
    check_file(json_out, overwrite=True)
    with open(json_out, mode="w") as fp:
        data: dict[str, Any] = {
            "parsed": parsed.model_dump(mode="json"),
            "expanded": expanded.model_dump(mode="json"),
        }
        json.dump(data, fp, indent=1)
    txt_out = json_out.with_suffix(".txt")
    txt_out.write_text(style.expanded_debug(parsed=parsed, expanded=expanded))
    return json_out


def all_page_lines(
    dir_out: Path,
    pages: Iterable[PageLines],
    data_type: DataType = DataType.JSON,
    overwrite: bool = False,
):
    """all_page_lines.

    Args:
        dir_out (Path): _description_
        pages (Iterable[PageLines]): _description_
        data_type (DataType, optional): _description_. Defaults to DataType.JSON.
        overwrite (bool, optional): _description_. Defaults to False.
    """
    for item in pages:
        _ = page_lines(
            dir_out=dir_out, page_lines=item, data_type=data_type, overwrite=overwrite
        )


def all_trip_lines(
    dir_out: Path,
    trips: Iterable[TripLines],
    data_type: DataType = DataType.JSON,
    overwrite: bool = False,
):
    """all_trip_lines.

    Args:
        dir_out (Path): _description_
        trips (Iterable[TripLines]): _description_
        data_type (DataType, optional): _description_. Defaults to DataType.JSON.
        overwrite (bool, optional): _description_. Defaults to False.
    """
    for item in trips:
        _ = trip_lines(
            dir_out=dir_out, trip_lines=item, data_type=data_type, overwrite=overwrite
        )


def all_parsed_trips(
    dir_out: Path,
    parsed: Iterable[ParsedTrip],
    data_type: DataType = DataType.JSON,
    overwrite: bool = False,
):
    """all_parsed_trips.

    Args:
        dir_out (Path): _description_
        parsed (Iterable[ParsedTrip]): _description_
        data_type (DataType, optional): _description_. Defaults to DataType.JSON.
        overwrite (bool, optional): _description_. Defaults to False.
    """
    for item in parsed:
        _ = parsed_trip(
            dir_out=dir_out, parsed_trip=item, data_type=data_type, overwrite=overwrite
        )


def all_expanded_trips(
    dir_out: Path,
    expanded: Iterable[ExpandedTrip],
    data_type: DataType = DataType.JSON,
    overwrite: bool = False,
):
    """all_expanded_trips.

    Args:
        dir_out (Path): _description_
        expanded (Iterable[ExpandedTrip]): _description_
        data_type (DataType, optional): _description_. Defaults to DataType.JSON.
        overwrite (bool, optional): _description_. Defaults to False.
    """
    for item in expanded:
        _ = expanded_trip(
            dir_out=dir_out,
            expanded_trip=item,
            data_type=data_type,
            overwrite=overwrite,
        )
