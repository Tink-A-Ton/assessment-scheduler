from datetime import date, timedelta
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
