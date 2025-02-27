"""FILE: load.py."""

from collections.abc import Iterable, Iterator
from pathlib import Path

import yaml

from pbs_parse.pbs_2022_01.api.common import DataType
from pbs_parse.pbs_2022_01.models.expanded import ExpandedTrip
from pbs_parse.pbs_2022_01.models.page_lines import PageLines
from pbs_parse.pbs_2022_01.models.parsed_trip import ParsedTrip
from pbs_parse.pbs_2022_01.models.trip_lines import TripLines


def page_lines(file_in: Path, data_type: DataType = DataType.JSON) -> PageLines:
    """page_lines.

    Args:
        file_in (Path): _description_
        data_type (DataType, optional): _description_. Defaults to DataType.JSON.

    Raises:
        ValueError: _description_
        ValueError: _description_

    Returns:
        PageLines: _description_
    """
    match data_type:
        case DataType.JSON:
            page = PageLines.model_validate_json(file_in.read_text())
        case DataType.YAML:
            with open(file=file_in) as fp:
                data = yaml.safe_load(fp)
            page = PageLines.model_validate(data)
        case DataType.TXT:
            raise ValueError("PageLines cannot be of type TXT.")
        case _:  # type: ignore
            raise ValueError(f"{data_type} is not a valid data type.")
    return page


def trip_lines(file_in: Path, data_type: DataType = DataType.JSON) -> TripLines:
    """trip_lines.

    Args:
        file_in (Path): _description_
        data_type (DataType, optional): _description_. Defaults to DataType.JSON.

    Raises:
        ValueError: _description_
        ValueError: _description_

    Returns:
        TripLines: _description_
    """
    match data_type:
        case DataType.JSON:
            trip = TripLines.model_validate_json(file_in.read_text())
        case DataType.YAML:
            with open(file=file_in) as fp:
                data = yaml.safe_load(fp)
            trip = TripLines.model_validate(data)
        case DataType.TXT:
            raise ValueError("TripLines cannot be of type TXT.")
        case _:  # type: ignore
            raise ValueError(f"{data_type} is not a valid data type.")
    return trip


def parsed_trip(file_in: Path, data_type: DataType = DataType.JSON) -> ParsedTrip:
    """parsed_trip.

    Args:
        file_in (Path): _description_
        data_type (DataType, optional): _description_. Defaults to DataType.JSON.

    Raises:
        ValueError: _description_
        ValueError: _description_

    Returns:
        ParsedTrip: _description_
    """
    match data_type:
        case DataType.JSON:
            parsed = ParsedTrip.model_validate_json(file_in.read_text())
        case DataType.YAML:
            with open(file=file_in) as fp:
                data = yaml.safe_load(fp)
            parsed = ParsedTrip.model_validate(data)
        case DataType.TXT:
            raise ValueError("ParsedTrip cannot be of type TXT.")
        case _:  # type: ignore
            raise ValueError(f"{data_type} is not a valid data type.")
    return parsed


def expanded_trip(file_in: Path, data_type: DataType = DataType.JSON) -> ExpandedTrip:
    """expanded_trip.

    Args:
        file_in (Path): _description_
        data_type (DataType, optional): _description_. Defaults to DataType.JSON.

    Raises:
        ValueError: _description_
        ValueError: _description_

    Returns:
        ExpandedTrip: _description_
    """
    match data_type:
        case DataType.JSON:
            expanded = ExpandedTrip.model_validate_json(file_in.read_text())
        case DataType.YAML:
            with open(file=file_in) as fp:
                data = yaml.safe_load(fp)
            expanded = ExpandedTrip.model_validate(data)
        case DataType.TXT:
            raise ValueError("ExpandedTrip cannot be of type TXT.")
        case _:  # type: ignore
            raise ValueError(f"{data_type} is not a valid data type.")
    return expanded


def all_page_lines(
    files_in: Iterable[Path], data_type: DataType = DataType.JSON
) -> Iterator[PageLines]:
    """all_page_lines.

    Args:
        files_in (Iterable[Path]): _description_
        data_type (DataType, optional): _description_. Defaults to DataType.JSON.

    Yields:
        Iterator[PageLines]: _description_
    """
    for file_path in files_in:
        yield page_lines(file_in=file_path, data_type=data_type)


def all_trip_lines(
    files_in: Iterable[Path], data_type: DataType = DataType.JSON
) -> Iterator[TripLines]:
    """all_trip_lines.

    Args:
        files_in (Iterable[Path]): _description_
        data_type (DataType, optional): _description_. Defaults to DataType.JSON.

    Yields:
        Iterator[TripLines]: _description_
    """
    for file_path in files_in:
        yield trip_lines(file_in=file_path, data_type=data_type)


def all_parsed_trips(
    files_in: Iterable[Path], data_type: DataType = DataType.JSON
) -> Iterator[ParsedTrip]:
    """all_parsed_trips.

    Args:
        files_in (Iterable[Path]): _description_
        data_type (DataType, optional): _description_. Defaults to DataType.JSON.

    Yields:
        Iterator[ParsedTrip]: _description_
    """
    for file_path in files_in:
        yield parsed_trip(file_in=file_path, data_type=data_type)


def all_expanded_trips(
    files_in: Iterable[Path], data_type: DataType = DataType.JSON
) -> Iterator[ExpandedTrip]:
    """all_expanded_trips.

    Args:
        files_in (Iterable[Path]): _description_
        data_type (DataType, optional): _description_. Defaults to DataType.JSON.

    Yields:
        Iterator[ExpandedTrip]: _description_
    """
    for file_path in files_in:
        yield expanded_trip(file_in=file_path, data_type=data_type)
