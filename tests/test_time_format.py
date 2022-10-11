from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import pytest

from now.time_format import parse


def current_datetime(*args, **kwargs):
    if "microsecond" not in kwargs:
        kwargs["microsecond"] = 0
    return datetime.now().replace(*args, **kwargs)


@pytest.mark.parametrize(
    "time, expected",
    [
        ("2006", datetime(year=2006, month=1, day=1)),
        ("2006-1", datetime(year=2006, month=1, day=1)),
        ("2006-1-2", datetime(year=2006, month=1, day=2)),
        ("2006-1-2 15", datetime(year=2006, month=1, day=2, hour=15)),
        ("2006-1-2 15:4", datetime(year=2006, month=1, day=2, hour=15, minute=4)),
        (
            "2006-1-2 15:4:5",
            datetime(year=2006, month=1, day=2, hour=15, minute=4, second=5),
        ),
        ("1-2", datetime(year=1900, month=1, day=2)),
        ("15:4:5", datetime(year=1900, month=1, day=1, hour=15, minute=4, second=5)),
        ("15:4", datetime(year=1900, month=1, day=1, hour=15, minute=4)),
        ("15", datetime(year=1900, month=1, day=1, hour=15)),
        (
            "2006-01-02T15:04:05Z-0700",
            datetime(
                year=2006,
                month=1,
                day=2,
                hour=15,
                minute=4,
                second=5,
                tzinfo=timezone(timedelta(hours=-7)),
            ),
        ),
        ("2006.1.2", datetime(year=2006, month=1, day=2)),
        (
            "2006.1.2 15:04:05",
            datetime(year=2006, month=1, day=2, hour=15, minute=4, second=5),
        ),
        (
            "2006.1.2 15:04:05.999999",
            datetime(
                year=2006,
                month=1,
                day=2,
                hour=15,
                minute=4,
                second=5,
                microsecond=999999,
            ),
        ),
        ("1/2/2006", datetime(year=2006, month=1, day=2)),
        (
            "1/2/2006 15:4:5",
            datetime(year=2006, month=1, day=2, hour=15, minute=4, second=5),
        ),
        ("2006/01/02", datetime(year=2006, month=1, day=2)),
        ("20060102", datetime(year=2006, month=1, day=2)),
        (
            "2006/01/02 15:04:05",
            datetime(year=2006, month=1, day=2, hour=15, minute=4, second=5),
        ),
        (
            "Mon Jan 2 15:04:05 2006",
            datetime(year=2006, month=1, day=2, hour=15, minute=4, second=5),
        ),
        (
            "Mon Jan 02 15:04:05 -0700 2006",
            datetime(
                year=2006,
                month=1,
                day=2,
                hour=15,
                minute=4,
                second=5,
                tzinfo=timezone(timedelta(hours=-7)),
            ),
        ),
        (
            "02 Jan 06 15:04 -0700",
            datetime(
                year=2006,
                month=1,
                day=2,
                hour=15,
                minute=4,
                tzinfo=timezone(timedelta(hours=-7)),
            ),
        ),
        (
            "Mon, 02 Jan 2006 15:04:05 -0700",
            datetime(
                year=2006,
                month=1,
                day=2,
                hour=15,
                minute=4,
                second=5,
                tzinfo=timezone(timedelta(hours=-7)),
            ),
        ),
        ("3:04PM", datetime(year=1900, month=1, day=1, hour=15, minute=4)),
        (
            "Jan 2 15:04:05",
            datetime(year=1900, month=1, day=2, hour=15, minute=4, second=5),
        ),
        (
            "Jan 2 15:04:05.000",
            datetime(
                year=1900, month=1, day=2, hour=15, minute=4, second=5, microsecond=0
            ),
        ),
        (
            "Jan 2 15:04:05.000000",
            datetime(
                year=1900,
                month=1,
                day=2,
                hour=15,
                minute=4,
                second=5,
                microsecond=000000,
            ),
        ),
    ],
)
def test_parse(time, expected):
    assert parse(time) == expected


@pytest.mark.parametrize(
    "time, expected",
    [
        ("2006", current_datetime(year=2006)),
        ("2006-1", current_datetime(year=2006, month=1)),
        ("2006-1-2", current_datetime(year=2006, month=1, day=2)),
        ("2006-1-2 15", current_datetime(year=2006, month=1, day=2, hour=15)),
        (
            "2006-1-2 15:4",
            current_datetime(year=2006, month=1, day=2, hour=15, minute=4),
        ),
    ],
)
def test_parse_current_time(time, expected):
    assert parse(time, date_time=datetime.now().replace(microsecond=0)) == expected


def test_parse_invalid_time():
    with pytest.raises(ValueError):
        parse("11:00:00 AM")
