"""FILE: validator.py."""

import logging
from dataclasses import asdict
from pathlib import Path
from pprint import pformat

from pbs_parse.pbs_2022_01.models import expanded as ET
from pbs_parse.pbs_2022_01.models import structured as ST
from pbs_parse.pbs_2022_01.models.parsed_trip import PARSED_TRIP_SERIALIZER

logger = logging.getLogger(__name__)


class ExpandedValidator:
    """A validator for expanded trips."""

    def __init__(
        self,
        expanded_trip: ET.ExpandedTrip,
        structured_trip: ST.StructuredTrip,
        expanded_trip_path: Path | None = None,
        structured_trip_path: Path | None = None,
        parsed_trip_path: Path | None = None,
    ) -> None:
        """__init__.

        Args:
            expanded_trip (ET.ExpandedTrip): _description_
            structured_trip (ST.StructuredTrip): _description_
            expanded_trip_path (Path | None, optional): _description_. Defaults to None.
            structured_trip_path (Path | None, optional): _description_. Defaults to None.
            parsed_trip_path (Path | None, optional): _description_. Defaults to None.
        """
        self.expanded_trip = expanded_trip
        self.structured_trip = structured_trip
        self.expanded_trip_path = expanded_trip_path
        self.structured_trip_path = structured_trip_path
        self.parsed_trip_path = parsed_trip_path
        self.errors: list[str] = []

    def validate(self) -> None:
        """Validate."""
        self._validate()

    def __str__(self) -> str:
        """Custom str output."""
        parsed_trip_str = ""
        if self.parsed_trip_path is not None:
            try:
                parsed_trip = PARSED_TRIP_SERIALIZER.load_from_json(
                    self.parsed_trip_path
                )
                parsed_trip_str = str(parsed_trip)
            except Exception:
                logger.exception(
                    "Tried to load parsed trip from %s but got error.",
                    self.parsed_trip_path,
                )
        return (
            f"Errors:\n{"\n".join(self.errors)}"
            f"\nParsed Trip:\n{parsed_trip_str}"
            f"\nexpanded_path: {self.expanded_trip_path}\nstructured path: {self.structured_trip_path}\n"
            f"{self.expanded_trip}\n\n{pformat(asdict(self.structured_trip),sort_dicts=False)}"
        )

    def _validate(self) -> None:
        """Validator functions called from here."""
        self._check_localized_times()
        return None

    def _check_localized_times(self) -> None:
        """Check that the localized utc times match the structured trip times."""
        hb_tz_name = self.expanded_trip.base_equipment.base.tz_name
        for dp_idx, dutyperiods in enumerate(
            zip(
                self.expanded_trip.dutyperiods,
                self.structured_trip.dutyperiods,
                strict=True,
            ),
            start=1,
        ):
            dp_errors = self._check_dutyperiod_times(
                expanded_dp=dutyperiods[0],
                structured_dp=dutyperiods[1],
                hb_tz_name=hb_tz_name,
                dp_idx=dp_idx,
            )
            self.errors.extend(dp_errors)
            for flt_idx, flights in enumerate(
                zip(dutyperiods[0].flights, dutyperiods[1].flights, strict=True),
                start=1,
            ):
                flt_errors = self._check_flight_times(
                    expanded_flt=flights[0],
                    structured_flt=flights[1],
                    hb_tz_name=hb_tz_name,
                    dp_idx=dp_idx,
                    flt_idx=flt_idx,
                )
                self.errors.extend(flt_errors)

    def _check_dutyperiod_times(
        self,
        expanded_dp: ET.DutyPeriod,
        structured_dp: ST.DutyPeriod,
        hb_tz_name: str,
        dp_idx: int,
    ) -> list[str]:
        """Check the dutyperiod report and release times."""
        errors: list[str] = []
        tests = [
            (expanded_dp.report_lcl, structured_dp.report_time.lcl, "local report"),
            # (expanded_dp.report_hbt, structured_dp.report_time.hbt, "hbt report"),
            (expanded_dp.release_lcl, structured_dp.release_time.lcl, "local release"),
            # (expanded_dp.release_hbt, structured_dp.release_time.hbt, "hbt release"),
        ]
        for test in tests:
            if test[0].strftime("%H%M") != test[1]:
                errors.append(
                    f"Expanded {test[0].isoformat()} time does not match Structured {test[1]}"
                    f" for dutyperiod idx {dp_idx}, field `{test[2]}`"
                )

        return errors

    def _check_flight_times(
        self,
        expanded_flt: ET.Flight,
        structured_flt: ST.Flight,
        hb_tz_name: str,
        dp_idx: int,
        flt_idx: int,
    ) -> list[str]:
        """Check the flight departure and arrival times."""
        errors: list[str] = []
        tests = [
            (
                expanded_flt.departure_lcl,
                structured_flt.departure_time.lcl,
                "local departure",
            ),
            # (expanded_flt.departure_hbt, structured_flt.departure_time.hbt, "hbt departure"),
            (
                expanded_flt.arrival_lcl,
                structured_flt.arrival_time.lcl,
                "local arrival",
            ),
            # (expanded_flt.arrival_hbt, structured_flt.arrival_time.hbt, "hbt arrival"),
        ]

        for test in tests:
            if test[0].strftime("%H%M") != test[1]:
                errors.append(
                    f"Expanded {test[0].isoformat()} time does not match Structured "
                    f"{test[1]} for dutyperiod-{dp_idx} flight-{flt_idx} field `{test[2]}`"
                )

        return errors
