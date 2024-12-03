import click
from flask.cli import AppGroup
from rich.console import Console
from rich.table import Table
from App.controllers import get_exams,detect_exam_clash,create_exam,parse_date,parse_time,get_course,get_courses
from flask import current_app

rule_set: list[str|None] = ["rule1","rule2"] #all rules enabled by default
console = Console()
exam = AppGroup("exam", help="Commands that relate to the management of examinations with all commands having a customisable rule setting")


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


@exam.command("ls", help="This command shows the list of all existing exams based on the customisable rule setting")
@click.argument("rule_setting", default="all", callback=setting_checker, type=click.Choice(["1", "2", "all", "none"], case_sensitive=False))
def ls(rule_setting):
    console.print("\n")
    results = get_exams()

    rule_set_handler(rule_setting)

    table = Table(title="Existing Examinations")
    table.add_column("Course Code", style="yellow")
    table.add_column("Start Date", style="magenta")
    table.add_column("Start Time", style="magenta")
    table.add_column("End Time", style="magenta")
    table.add_column("Clash?", style="cyan")
    for result in results:
        detect_exam_clash(result)
        table.add_row(result.course_code, str(result.start_date), str(result.start_time), str(result.end_time), str(result.clash_detected))
    console.print(table)
    console.print("\n")

@exam.command("clashes", help="This command shows the list of all CLASHING exams with customisable rule setting")
@click.argument("rule_setting", default="all", callback=setting_checker, type=click.Choice(["1", "2", "all", "none"], case_sensitive=False))
def clashes(rule_setting):
    console.print("\n")
    results = get_exams()
    
    rule_set_handler(rule_setting)

    table = Table(title="Clashing Examinations")
    table.add_column("Course Code", style="yellow")
    table.add_column("Start Date", style="magenta")
    table.add_column("Start Time", style="magenta")
    table.add_column("End Time", style="magenta")
    table.add_column("Clash?", style="cyan")
    for result in results:
        if detect_exam_clash(result,rule_set[0],rule_set[1]):
            table.add_row(result.course_code, str(result.start_date), str(result.start_time), str(result.end_time), str(result.clash_detected))
    console.print(table)
    console.print("\n")

@exam.command("schedule", help="Schedules an exam or shows if a clash exists with customisable rule setting")
@click.argument("course", callback=course_checker)
@click.argument("date", callback=date_checker)
@click.argument("start_time", callback=time_checker)
@click.argument("end_time", callback=time_checker)
@click.argument("rule_setting", default="all", callback=setting_checker, type=click.Choice(["1", "2", "all", "none"], case_sensitive=False))
def schedule(course,date,start_time,end_time,rule_setting):
    console.print("\n")

    rule_set_handler(rule_setting)

    date = parse_date(date)
    start_time = parse_time(start_time)
    end_time = parse_time(end_time)
    exam = create_exam(course, date, start_time, end_time)
    if detect_exam_clash(exam,rule_set[0],rule_set[1]):
        console.print("[red]ERROR! Clash Detected!")
    else:
        console.print(f"[green]Exam for {course} scheduled on {date} from {start_time} to {end_time}")
    console.print("\n")