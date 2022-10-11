from datetime import datetime

import pytest

from now.now import Now, WeekStartDay


@pytest.fixture
def now():
    time = datetime(year=2022, month=10, day=11, hour=10, minute=30, second=15)

    return Now(time)


def test_now():
    assert Now().time < datetime.now()


def test_str(now):
    assert "2022-10-11 10:30:15" == str(now)


def test_time(now):
    assert now.time == datetime(
        year=2022, month=10, day=11, hour=10, minute=30, second=15
    )

    new_value = now.time.replace(hour=11)

    now.time = new_value

    assert now.time == new_value


def test_time_format(now):
    with pytest.raises(ValueError):
        assert now.parse("~10:30~")

    now.time_formats = ["~%H:%M~"]

    assert now.time_formats == ["~%H:%M~"]

    assert now.parse("~10:30~") == now.time.replace(hour=10, minute=30)


def test_quarter(now):
    assert now.quarter() == 4


def test_half(now):
    assert now.half() == 2


def test_beginning_of_minute(now):
    assert now.beginning_of_minute() == datetime(
        year=2022, month=10, day=11, hour=10, minute=30, second=0
    )


def test_beginning_of_hour(now):
    assert now.beginning_of_hour() == datetime(
        year=2022, month=10, day=11, hour=10, minute=0, second=0
    )


def test_beginning_of_day(now):
    assert now.beginning_of_day() == datetime(
        year=2022, month=10, day=11, hour=0, minute=0, second=0
    )


def test_beginning_of_week(now):
    assert now.beginning_of_week() == datetime(
        year=2022, month=10, day=9, hour=0, minute=0, second=0
    )

    assert now.week_start_day == WeekStartDay.SUNDAY

    now.week_start_day = WeekStartDay.MONDAY

    assert now.beginning_of_week() == datetime(
        year=2022, month=10, day=10, hour=0, minute=0, second=0
    )


def test_beginning_of_month(now):
    assert now.beginning_of_month() == datetime(
        year=2022, month=10, day=1, hour=0, minute=0, second=0
    )


def test_beginning_of_quarter(now):
    assert now.beginning_of_quarter() == datetime(
        year=2022, month=10, day=1, hour=0, minute=0, second=0
    )


def test_beginning_of_half(now):
    assert now.beginning_of_half() == datetime(
        year=2022, month=7, day=1, hour=0, minute=0, second=0
    )


def test_beginning_of_year(now):
    assert now.beginning_of_year() == datetime(
        year=2022, month=1, day=1, hour=0, minute=0, second=0
    )


def test_end_of_minute(now):
    assert now.end_of_minute() == datetime(
        year=2022, month=10, day=11, hour=10, minute=30, second=59, microsecond=999999
    )


def test_end_of_hour(now):
    assert now.end_of_hour() == datetime(
        year=2022, month=10, day=11, hour=10, minute=59, second=59, microsecond=999999
    )


def test_end_of_day(now):
    assert now.end_of_day() == datetime(
        year=2022, month=10, day=11, hour=23, minute=59, second=59, microsecond=999999
    )


def test_end_of_week(now):
    assert now.end_of_week() == datetime(
        year=2022, month=10, day=15, hour=23, minute=59, second=59, microsecond=999999
    )


def test_end_of_month(now):
    assert now.end_of_month() == datetime(
        year=2022, month=10, day=31, hour=23, minute=59, second=59, microsecond=999999
    )


def test_end_of_quarter(now):
    assert now.end_of_quarter() == datetime(
        year=2022, month=12, day=31, hour=23, minute=59, second=59, microsecond=999999
    )


def test_end_of_half(now):
    assert now.end_of_half() == datetime(
        year=2022, month=12, day=31, hour=23, minute=59, second=59, microsecond=999999
    )


def test_end_of_year(now):
    assert now.end_of_year() == datetime(
        year=2022, month=12, day=31, hour=23, minute=59, second=59, microsecond=999999
    )


def test_monday(now):
    assert now.monday() == datetime(
        year=2022, month=10, day=10, hour=0, minute=0, second=0
    )

    assert now.monday("10-9") == now.time.replace(month=10, day=8)


def test_sunday(now):
    assert now.sunday() == datetime(
        year=2022, month=10, day=9, hour=0, minute=0, second=0
    )

    assert now.sunday("10-9") == now.time.replace(month=10, day=7)


def test_parse(now):
    assert now.parse("20:45") == datetime(
        year=2022, month=10, day=11, hour=20, minute=45, second=15
    )


def test_between(now):
    assert now.between("9:30", "12:15")
    assert not now.between("8:45", "10:00")


def test_week_range(now):
    now.week_start_day = WeekStartDay.SUNDAY

    for i in range(7, 14):
        now.time = now.time.replace(day=i)

        if i <= 8:
            time = datetime(year=2022, month=10, day=2)
        else:
            time = datetime(year=2022, month=10, day=9)
        assert now.beginning_of_week() == time

        if i <= 8:
            time = datetime(year=2022, month=10, day=8, hour=23, minute=59, second=59, microsecond=999999)
        else:
            time = datetime(year=2022, month=10, day=15, hour=23, minute=59, second=59, microsecond=999999)
        assert now.end_of_week() == time

    now.week_start_day = WeekStartDay.MONDAY

    for i in range(7, 14):
        now.time = now.time.replace(day=i)

        if i <= 9:
            time = datetime(year=2022, month=10, day=3)
        else:
            time = datetime(year=2022, month=10, day=10)
        assert now.beginning_of_week() == time

        if i <= 9:
            time = datetime(year=2022, month=10, day=9, hour=23, minute=59, second=59, microsecond=999999)
        else:
            time = datetime(year=2022, month=10, day=16, hour=23, minute=59, second=59, microsecond=999999)
        assert now.end_of_week() == time
