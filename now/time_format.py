import contextlib
import enum
import functools
from datetime import datetime


class Time(enum.IntEnum):
    YEAR = 0b00000001
    MONTH = 0b00000010
    DAY = 0b00000100

    HOUR = 0b00001000
    MINUTE = 0b00010000
    SECOND = 0b00100000
    MICROSECOND = 0b01000000
    TZINFO = 0b10000000

    DATE = YEAR | MONTH | DAY
    TIME = HOUR | MINUTE | SECOND | MICROSECOND | TZINFO

    ALL = DATE | TIME


TIME_FORMATS = [
    "%Y",
    "%Y-%m",
    "%Y-%m-%d",
    "%Y-%m-%d %H",
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d %H:%M:%S",
    "%m-%d",
    "%H:%M:%S",
    "%H:%M",
    "%H",
    "%Y-%m-%dT%H:%M:%SZ%z",
    "%Y.%m.%d",
    "%Y.%m.%d %H:%M:%S",
    "%Y.%m.%d %H:%M:%S.%f",
    "%m/%d/%Y",
    "%m/%d/%Y %H:%M:%S",
    "%Y/%m/%d",
    "%Y%m%d",
    "%Y/%m/%d %H:%M:%S",
    "%a %b %d %H:%M:%S %Y",  # ANSIC
    "%a %b %d %H:%M:%S %z %Y",  # RubyDate
    "%d %b %y %H:%M %z",  # RFC822Z
    "%a, %d %b %Y %H:%M:%S %z",  # RFC1123Z
    "%I:%M%p",  # Kitchen
    "%b %d %H:%M:%S",  # Stamp
    "%b %d %H:%M:%S.%f",  # StampMilli, StampMicro
]


FORMAT_CODES: dict[str, Time] = {
    "%d": Time.DAY,
    "%b": Time.MONTH,
    "%B": Time.MONTH,
    "%m": Time.MONTH,
    "%y": Time.YEAR,
    "%Y": Time.YEAR,
    "%H": Time.HOUR,
    "%I": Time.HOUR,
    "%M": Time.MINUTE,
    "%S": Time.SECOND,
    "%f": Time.MICROSECOND,
    "%z": Time.TZINFO,
}


@functools.lru_cache()
def format_defaults(time_format: str) -> int:
    defaults: int = Time.ALL
    for code in FORMAT_CODES:
        if code in time_format:
            defaults ^= FORMAT_CODES[code]
    return defaults


def parse(
    string: str, default_time: datetime | None = None, formats: list[str] | None = None
) -> datetime:
    formats = formats or TIME_FORMATS

    for time_format in formats:

        with contextlib.suppress(ValueError):
            time = datetime.strptime(string, time_format)

            if not default_time:
                return time

            defaults = format_defaults(time_format)

            if defaults:
                if defaults & Time.YEAR:
                    time = time.replace(year=default_time.year)
                if defaults & Time.MONTH:
                    time = time.replace(month=default_time.month)
                if defaults & Time.DAY:
                    time = time.replace(day=default_time.day)
                if defaults & Time.HOUR:
                    time = time.replace(hour=default_time.hour)
                if defaults & Time.MINUTE:
                    time = time.replace(minute=default_time.minute)
                if defaults & Time.SECOND:
                    time = time.replace(second=default_time.second)
                if defaults & Time.MICROSECOND:
                    time = time.replace(microsecond=default_time.microsecond)
                if defaults & Time.TZINFO:
                    time = time.replace(tzinfo=default_time.tzinfo)

            return time

    raise ValueError(f"Can't parse string as time: {string!r}")
