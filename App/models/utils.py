from datetime import date, datetime, time, timedelta
from enum import Enum


class Position(Enum):
    PTINSTRUCTOR = "Part-Time Instructor"
    INSTRUCTOR = "Instructor"
    HOD = "Head of Department"
    LECTURER = "Lecturer"
    TA = "Teaching Assistant"
    TUTOR = "Tutor"
    PTTUTOR = "Part-Time Tutor"


def get_week_range(date_str: str) -> tuple[date, date]:
    """Sunday - Saturday Week"""
    input_date: date = date.fromisoformat(date_str)
    start_of_week: date = input_date - timedelta(days=(input_date.weekday() + 1) % 7)
    end_of_week: date = start_of_week + timedelta(days=6)
    return start_of_week, end_of_week


def parse_date(date_str) -> None | date:
    if date_str == "":
        return None
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def parse_time(time_str) -> None | time:
    if time_str == "":
        return None
    time_str = time_str[:5]
    return datetime.strptime(time_str, "%H:%M").time()
