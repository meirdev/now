from datetime import datetime

import now


def test_main():
    now.quarter()
    now.half()
    now.beginning_of_minute()
    now.beginning_of_hour()
    now.beginning_of_day()
    now.beginning_of_week()
    now.beginning_of_month()
    now.beginning_of_quarter()
    now.beginning_of_half()
    now.beginning_of_year()
    now.end_of_minute()
    now.end_of_hour()
    now.end_of_day()
    now.end_of_week()
    now.end_of_month()
    now.end_of_quarter()
    now.end_of_half()
    now.end_of_year()
    now.monday("12:00")
    now.sunday("12:30")
    now.parse("12:30")
    now.between("12:30", "13:00")
    now.with_(datetime(2022, 10, 11, 10, 30, 0)).quarter()
