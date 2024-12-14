"""json encoder that handles more complex types."""

import datetime
import json
from typing import Any

from ..datetime.iso8601_datetime import serialize_dt
from ..datetime.iso8601_duration import timedelta_to_isoformat


class DateTimeIsoEncoderSimple(json.JSONEncoder):
    """DateTimeEncoder."""

    def default(self, o: Any):
        """Converts to iso format.

        https://stackoverflow.com/a/12126976
        """
        if isinstance(o, datetime.datetime | datetime.date | datetime.time):
            return o.isoformat()
        elif isinstance(o, datetime.timedelta):
            return timedelta_to_isoformat(o)

        return super().default(o)


class DateTimeIsoEncoder(json.JSONEncoder):
    """DateTimeEncoder."""

    def default(self, o: Any):
        """Converts to iso format.

        https://stackoverflow.com/a/12126976
        """
        if isinstance(o, datetime.datetime):
            return serialize_dt(value=o)
        if isinstance(o, datetime.date | datetime.time):
            return o.isoformat()
        elif isinstance(o, datetime.timedelta):
            return timedelta_to_isoformat(o)

        return super().default(o)
