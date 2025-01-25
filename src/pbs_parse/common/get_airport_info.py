"""FILE: get_airport_code.py."""

from pbs_parse.airports import airport_from_iata
from pbs_parse.pbs_2022_01.models.expanded import AirportInfo


def get_airport_info_from_iata(iata: str) -> AirportInfo:
    """Get airport info from database."""
    airport = airport_from_iata(iata=iata)
    return AirportInfo(
        iata=airport["iata"], icao=airport["icao"], tz_name=airport["tz"]
    )
