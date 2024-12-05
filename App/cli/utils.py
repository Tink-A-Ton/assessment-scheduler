import click
from rich.console import Console
from rich.table import Table
from ..controllers import (
    get_staff,
    get_all_staff,
    parse_date,
    parse_time,
    get_course,
    get_courses,
)
from flask import current_app
from ..models import Exam

console = Console()

rule_set: list[str | None] = ["rule1", "rule2"]  # all rules enabled by default


def date_checker(ctx, param, value):
    try:
        parse_date(value)
    except:
        raise click.BadParameter(
            f"Date {value} is invalid format for 'YYYY-MM-DD'",
            param_hint="date in correct format",
        )
    return value


def time_checker(ctx, param, value):
    try:
        parse_time(value)
    except:
        raise click.BadParameter(
            f"Time {value} is invalid format for 'HH:MM'",
            param_hint="time in correct format",
        )
    return value


def course_checker(ctx, param, value):
    with current_app.app_context():
        if not get_course(value):
            raise click.BadParameter(
                f"Course does NOT Exist", param_hint="existing course code"
            )
    return value


def course_not_exist_checker(ctx, param, value):
    with current_app.app_context():
        if get_course(value):
            raise click.BadParameter(
                f"Course Already Exists", param_hint="non existing course code"
            )
    return value


def setting_checker(ctx, param, value):
    if value != "1" and value != "2" and value != "all" and value != "none":
        raise click.BadParameter(
            f"The setting for the ruleset must either be '1', '2', 'all' or 'none'"
        )
    return value


def course_list():
    with current_app.app_context():
        courses = get_courses()
        return [str(course) for course in courses]


def staff_id_array():
    with current_app.app_context():
        staff = get_all_staff()
        return [str(staff_member.id) for staff_member in staff]


def staff_id_checker(ctx, param, value):
    with current_app.app_context():
        try:
            if not get_staff(int(value)):
                raise click.BadParameter(
                    f"invalid ID of '{value}'", param_hint="must be valid staff id"
                )
        except:
            raise click.BadParameter(
                f"invalid ID of '{value}'", param_hint="must be valid staff id"
            )
        return value


def rule_set_handler(setting):
    if setting == "1":
        rule_set[0] = "rule1"
        rule_set[0] = None
    elif setting == "2":
        rule_set[0] = None
        rule_set[1] = "rule2"
    elif setting == "all":
        rule_set[0] = "rule1"
        rule_set[1] = "rule2"
    else:  # none
        rule_set[0] = None
        rule_set[1] = None
    console.print(
        f"[magenta]Rule 1 Enabled: {bool(rule_set[0])}\nRule 2 Enabled: {bool(rule_set[1])}"
    )


def rule_setting_prompt():
    console.print(
        "[yellow]Rule 1: Prevents too many exams of the same level in the same week"
    )
    console.print(
        "[yellow]Rule 2: Prevents exam clashes within the same programme for courses on the same day."
    )
    console.print("\n")
    rule_setting = setting_checker(
        None,
        None,
        click.prompt(
            "Select Clash Rules",
            default="all",
            type=click.Choice(["1", "2", "all", "none"], case_sensitive=False),
            show_default=True,
            show_choices=True,
        ),
    )
    rule_set_handler(rule_setting)


def print_exams_table(title: str, exams: list[Exam]) -> None:
    table = Table(title=title)
    table.add_column("Course Code", style="yellow")
    table.add_column("Start Date", style="magenta")
    table.add_column("Start Time", style="magenta")
    table.add_column("End Time", style="magenta")
    table.add_column("Clash?", style="cyan")
    for exam in exams:
        table.add_row(
            exam.course_code,
            str(exam.start_date),
            str(exam.start_time),
            str(exam.end_time),
            str(exam.clash_detected),
        )
    console.print(table)
