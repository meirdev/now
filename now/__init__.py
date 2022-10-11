from datetime import datetime, tzinfo

from .now import Now, WeekStartDay
from .time_format import TIME_FORMATS

week_start_day: WeekStartDay = WeekStartDay.SUNDAY

time_zone: tzinfo | None = None

time_formats: list[str] = TIME_FORMATS


def with_(time: datetime | None = None) -> Now:
    if time is None:
        time = datetime.now(tz=time_zone)

    return Now(
        time=time,
        time_formats=time_formats,
        week_start_day=week_start_day,
    )


def quarter() -> int:
    return with_().quarter()


def half() -> int:
    return with_().half()


def beginning_of_minute() -> datetime:
    return with_().beginning_of_minute()


def beginning_of_hour() -> datetime:
    return with_().beginning_of_hour()


def beginning_of_day() -> datetime:
    return with_().beginning_of_day()


def beginning_of_week() -> datetime:
    return with_().beginning_of_week()


def beginning_of_month() -> datetime:
    return with_().beginning_of_month()


def beginning_of_quarter() -> datetime:
    return with_().beginning_of_quarter()


def beginning_of_half() -> datetime:
    return with_().beginning_of_half()


def beginning_of_year() -> datetime:
    return with_().beginning_of_year()


def end_of_minute() -> datetime:
    return with_().end_of_minute()


def end_of_hour() -> datetime:
    return with_().end_of_hour()


def end_of_day() -> datetime:
    return with_().end_of_day()


def end_of_week() -> datetime:
    return with_().end_of_week()


def end_of_month() -> datetime:
    return with_().end_of_month()


def end_of_quarter() -> datetime:
    return with_().end_of_quarter()


def end_of_half() -> datetime:
    return with_().end_of_half()


def end_of_year() -> datetime:
    return with_().end_of_year()


def monday(time: str) -> datetime:
    return with_().monday(time)


def sunday(time: str) -> datetime:
    return with_().sunday(time)


def parse(time: str) -> datetime:
    return with_().parse(time)


def between(begin: str, end: str) -> bool:
    return with_().between(begin, end)
