import calendar
import enum
from datetime import datetime, timedelta

from . import time_format


class Min(enum.IntEnum):
    MICROSECOND = 0
    SECOND = 0
    MINUTE = 0
    HOUR = 0
    DAY = 1
    MONTH = 1


class Max(enum.IntEnum):
    MICROSECOND = 999999
    SECOND = 59
    MINUTE = 59
    HOUR = 23
    DAY = 31
    MONTH = 12


class WeekStartDay(enum.IntEnum):
    SUNDAY = 0
    MONDAY = 1


class Now:
    def __init__(
        self,
        time: datetime | None = None,
        time_formats: list[str] | None = None,
        week_start_day: WeekStartDay = WeekStartDay.SUNDAY,
    ) -> None:
        if time is None:
            time = datetime.now()
        self._time: datetime = time

        if time_formats is None:
            time_formats = time_format.TIME_FORMATS
        self._time_formats: list[str] = time_formats

        self._week_start_day: WeekStartDay = week_start_day

    def __str__(self) -> str:
        return str(self._time)

    def _days_in_month(self, month: int) -> int:
        _, days = calendar.monthrange(self._time.year, month)

        return days

    def _week_range(self, week_start_day: WeekStartDay) -> tuple[timedelta, timedelta]:
        start_day = week_start_day
        now_day = (self._time.weekday() + 1) % 7

        if now_day < start_day:
            week_end = start_day - now_day
            week_start = 7 - week_end
        else:
            week_start = now_day - start_day
            week_end = 7 - week_start

        return timedelta(days=-week_start), timedelta(days=week_end - 1)

    @property
    def time(self) -> datetime:
        return self._time

    @time.setter
    def time(self, time: datetime) -> None:
        self._time = time

    @property
    def time_formats(self) -> list[str]:
        return self._time_formats

    @time_formats.setter
    def time_formats(self, time_formats: list[str]) -> None:
        self._time_formats = time_formats

    @property
    def week_start_day(self) -> WeekStartDay:
        return self._week_start_day

    @week_start_day.setter
    def week_start_day(self, week_start_day: WeekStartDay) -> None:
        self._week_start_day = week_start_day

    def quarter(self) -> int:
        return (self._time.month - 1) // 3 + 1

    def half(self) -> int:
        return (self._time.month - 1) // 6 + 1

    def beginning_of_minute(self) -> datetime:
        return self._time.replace(second=Min.SECOND, microsecond=Min.MICROSECOND)

    def beginning_of_hour(self) -> datetime:
        return self.beginning_of_minute().replace(minute=Min.MINUTE)

    def beginning_of_day(self) -> datetime:
        return self.beginning_of_hour().replace(hour=Min.HOUR)

    def beginning_of_week(self) -> datetime:
        days, _ = self._week_range(self._week_start_day)

        return self.beginning_of_day() + days

    def beginning_of_month(self) -> datetime:
        return self.beginning_of_day().replace(day=Min.DAY)

    def beginning_of_quarter(self) -> datetime:
        month = (self.quarter() - 1) * 3 + 1

        return self.beginning_of_month().replace(month=month)

    def beginning_of_half(self) -> datetime:
        month = (self.half() - 1) * 6 + 1

        return self.beginning_of_month().replace(month=month)

    def beginning_of_year(self) -> datetime:
        return self.beginning_of_month().replace(month=Min.MONTH)

    def end_of_minute(self) -> datetime:
        return self._time.replace(second=Max.SECOND, microsecond=Max.MICROSECOND)

    def end_of_hour(self) -> datetime:
        return self.end_of_minute().replace(minute=Max.MINUTE)

    def end_of_day(self) -> datetime:
        return self.end_of_hour().replace(hour=Max.HOUR)

    def end_of_week(self) -> datetime:
        _, days = self._week_range(self._week_start_day)

        return self.end_of_day() + days

    def end_of_month(self) -> datetime:
        day = self._days_in_month(self._time.month)

        return self.end_of_day().replace(day=day)

    def end_of_quarter(self) -> datetime:
        month = self.quarter() * 3
        day = self._days_in_month(month)

        return self.end_of_day().replace(month=month, day=day)

    def end_of_half(self) -> datetime:
        month = self.half() * 6
        day = self._days_in_month(month)

        return self.end_of_day().replace(month=month, day=day)

    def end_of_year(self) -> datetime:
        return self.end_of_day().replace(month=Max.MONTH, day=Max.DAY)

    def sunday(self, time: str | None = None) -> datetime:
        if time is not None:
            parsed_time = self.parse(time)
        else:
            parsed_time = self.beginning_of_day()

        days, _ = self._week_range(WeekStartDay.SUNDAY)

        return parsed_time + days

    def monday(self, time: str | None = None) -> datetime:
        if time is not None:
            parsed_time = self.parse(time)
        else:
            parsed_time = self.beginning_of_day()

        days, _ = self._week_range(WeekStartDay.MONDAY)

        return parsed_time + days

    def parse(self, time: str) -> datetime:
        return time_format.parse(time, self._time, self._time_formats)

    def between(self, begin: str, end: str) -> bool:
        begin_time = self.parse(begin)
        end_time = self.parse(end)

        return begin_time <= self._time <= end_time
