import sys
from typing import Optional
import click
from flask import Flask
from flask.cli import AppGroup
import pytest
from rich.console import Console
from rich.table import Table
from App.controllers import get_staff,get_all_staff,parse_date,parse_time,get_course,get_courses
from flask import current_app


def help_command(app: Flask, test: AppGroup) -> None:
    ctx = click.Context(app.cli)
    groups: dict[str, AppGroup] = {"test": test}
    table = Table(title="Available Commands")
    table.add_column("Command", justify="left", style="cyan", no_wrap=True)
    table.add_column("Description", justify="left", style="magenta")
    for cmd in app.cli.list_commands(ctx):
        command: Optional[click.Command] = app.cli.get_command(ctx, cmd)
        table.add_row(cmd, command.help if command else "No description available")
    for group_name, group in groups.items():
        for cmd in group.list_commands(ctx):
            command = group.get_command(ctx, cmd)
            table.add_row(
                f"{group_name} {cmd}",
                command.help if command else "No description available",
            )
    console = Console()
    console.print(table)


def run_tests(test_type: str, unit_key: str, integration_key: str) -> None:
    if test_type == "unit":
        sys.exit(pytest.main(["-k", unit_key]))
    elif test_type == "int":
        sys.exit(pytest.main(["-k", integration_key]))
    else:
        unit_result: int | pytest.ExitCode = pytest.main(["-k", unit_key])
        if unit_result == 0:
            integration_result: int | pytest.ExitCode = pytest.main(
                ["-k", integration_key]
            )
            sys.exit(integration_result)
        else:
            sys.exit(unit_result)


def run_all_tests() -> None:
    unit_result: int | pytest.ExitCode = pytest.main(["-k", "UnitTests"])
    if unit_result == 0:
        integration_result: int | pytest.ExitCode = pytest.main(
            ["-k", "IntegrationTests"]
        )
        sys.exit(integration_result)
    else:
        sys.exit(unit_result)


console = Console()

rule_set: list[str|None] = ["rule1","rule2"] #all rules enabled by default
def date_checker(ctx, param, value):
    try:
        parse_date(value)
    except:
        raise click.BadParameter(f"Date {value} is invalid format for 'YYYY-MM-DD'", param_hint="date in correct format")
    return value

def time_checker(ctx, param, value):
    try:
        parse_time(value)
    except:
        raise click.BadParameter(f"Time {value} is invalid format for 'HH:MM'", param_hint="time in correct format")
    return value

def course_checker(ctx, param, value):
    with current_app.app_context():
        if not get_course(value):
            raise click.BadParameter(f"Course does NOT Exist", param_hint="existing course code")
    return value

def course_not_exist_checker(ctx, param, value):
    with current_app.app_context():
        if get_course(value):
            raise click.BadParameter(f"Course Already Exists", param_hint="non existing course code")
    return value

def setting_checker(ctx, param, value):
    if value != "1" and value != "2" and value != "all" and value != "none":
        raise click.BadParameter(f"The setting for the ruleset must either be '1', '2', 'all' or 'none'")
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
                raise click.BadParameter(f"invalid ID of '{value}'", param_hint="must be valid staff id")
        except:
            raise click.BadParameter(f"invalid ID of '{value}'", param_hint="must be valid staff id")
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
    else: #none
        rule_set[0] = None
        rule_set[1] = None

def rule_set_print_info():
    console.print("\n")
    console.print("[yellow]Rule 1: Prevents too many exams of the same level in the same week")
    console.print("[yellow]Rule 2: Prevents exam clashes within the same programme for courses on the same day.")
    console.print(f"[magenta]Rule 1 Enabled: {bool(rule_set[0])}\nRule 2 Enabled: {bool(rule_set[1])}")
    console.print("[cyan]Use the rule_setting for this command (default='all' [1|2|all|none]) to customise which rules are enabled above :D")
    console.print("\n")