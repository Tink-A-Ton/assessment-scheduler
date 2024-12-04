import click
from rich.console import Console
from rich.table import Table
from App.controllers import get_staff,get_all_staff,parse_date,parse_time,get_course,get_courses
from flask import current_app


console = Console()

rule_set: list[str|None] = ["rule1","rule2"] #all rules enabled by default
def date_checker(ctx, param, value):
    try:
        parse_date(value)
    except:
        raise click.BadParameter(f"Date {value} is invalid format for 'YYYY-MM-DD'", param_hint="use correct format")
    return value

def time_checker(ctx, param, value):
    try:
        parse_time(value)
    except:
        raise click.BadParameter(f"Time {value} is invalid format for 'HH:MM'", param_hint="use correct format")
    return value

def course_checker(ctx, param, value):
    with current_app.app_context():
        if not get_course(value):
            raise click.BadParameter(f"Invalid Course given", param_hint="use an existing course")
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
    console.print("\n")
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
    console.print(f"[magenta]Rule 1 Enabled: {bool(rule_set[0])}\nRule 2 Enabled: {bool(rule_set[1])}")
    console.print("[cyan]Use the rule_setting for this command (default='all' [1|2|all|none]) to customise which rules are enabled above :D")
    console.print("\n")