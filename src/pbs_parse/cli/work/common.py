"""FILE: common.py."""

from pathlib import Path

from pbs_parse.pbs_2022_01.models.expanded import ExpandedTrip
from pbs_parse.pbs_2022_01.models.parsed_trip import PARSED_TRIP_SERIALIZER, ParsedTrip
from pbs_parse.pbs_2022_01.models.structured import (
    STRUCTURED_TRIP_SERIALIZER,
    StructuredTrip,
)
from pbs_parse.snippets.file.data_file_loader import FileResource


def load_parsed(parsed_dir: Path, s_trip: StructuredTrip) -> FileResource[ParsedTrip]:
    """load_parsed.

    Args:
        parsed_dir (Path): _description_
        s_trip (StructuredTrip): _description_

    Returns:
        FileResource[ParsedTrip]: _description_
    """
    parsed_name = ParsedTrip.assemble_file_name(idx=s_trip.idx, uuid=s_trip.source_uuid)
    path_in = parsed_dir / parsed_name
    parsed = PARSED_TRIP_SERIALIZER.load_from_json(path_in=path_in)
    return FileResource(resource=parsed, file_path=path_in)


def load_structured(
    structured_dir: Path, e_trip: ExpandedTrip
) -> FileResource[StructuredTrip]:
    """load_structured.

    Args:
        structured_dir (Path): _description_
        e_trip (ExpandedTrip): _description_

    Returns:
        FileResource[StructuredTrip]: _description_
    """
    structured_name = StructuredTrip.assemble_file_name(
        idx=e_trip.source_idx, uuid=e_trip.source_uuid
    )
    path_in = structured_dir / structured_name
    parsed = STRUCTURED_TRIP_SERIALIZER.load_from_json(path_in=path_in)
    return FileResource(resource=parsed, file_path=path_in)
