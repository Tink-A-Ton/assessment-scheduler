import click
from flask.cli import AppGroup
from rich.console import Console
from rich.table import Table
from ..models import Exam
from ..controllers import (
    get_exams,
    detect_exam_clash,
    create_exam,
    parse_date,
    parse_time,
)
from .utils import (
    date_checker,
    rule_setting_prompt,
    time_checker,
    course_checker,
    setting_checker,
    rule_set_handler,
    rule_set,
    print_exams_table,
)
from .course import list_courses

console = Console()
exam = AppGroup(
    "exam",
    help="Commands that relate to the management of examinations with all commands having a customisable rule setting",
)


@exam.command("list", help="Lists all existing exams")
def list_exams():
    console.print("\n")
    print_exams_table("Existing Exams", get_exams())
    console.print("\n")


@exam.command("clashes", help="Lists all clashes (based on given rule setting)")
def clashes():
    console.print("\n")
    rule_setting_prompt()
    exams: list[Exam] = get_exams()
    clashes: list[Exam] = []
    for exam in exams:
        if detect_exam_clash(exam, rule_set[0], rule_set[1]):
            clashes.append(exam)
    print_exams_table("Clashing Exams", clashes)
    console.print("\n")


@exam.command("schedule", help="Schedules an exam")
def schedule():
    console.print("\n")
    list_courses()
    course_code = course_checker(
        None, None, click.prompt("Course Code", default="COMP1700", show_default=True)
    )
    date = date_checker(
        None, None, click.prompt("Exam Date", default="2024-12-06", show_default=True)
    )
    start_time = time_checker(
        None, None, click.prompt("Exam Start Time", default="08:00", show_default=True)
    )
    end_time = time_checker(
        None, None, click.prompt("Exam End Time", default="10:00", show_default=True)
    )
    rule_setting_prompt()
    exam = create_exam(
        course_code, parse_date(date), parse_time(start_time), parse_time(end_time)
    )
    if detect_exam_clash(exam, rule_set[0], rule_set[1]):
        console.print("[red]ERROR! Clash Detected!")
    else:
        console.print(
            f"[green]Exam for {course_code} scheduled on {date} from {start_time} to {end_time}"
        )
    console.print("\n")
