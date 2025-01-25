"""FILE: common.py."""

from dataclasses import dataclass

# def load_parsed(parsed_dir: Path, s_trip: StructuredTrip) -> FileResource[ParsedTrip]:
#     """load_parsed.

#     Args:
#         parsed_dir (Path): _description_
#         s_trip (StructuredTrip): _description_

#     Returns:
#         FileResource[ParsedTrip]: _description_
#     """
#     # parsed_name = ParsedTrip.assemble_file_name(idx=s_trip.idx, uuid=s_trip.source_uuid)
#     path_in = parsed_dir / s_trip.source.parsed_trip
#     parsed = PARSED_TRIP_SERIALIZER.load_from_json(path_in=path_in)
#     return FileResource(resource=parsed, file_path=path_in)


@dataclass(slots=True)
class KeyedResource[T]:
    """KeyedResource."""

    resource: T
    key: str
