import click
from flask.cli import AppGroup
from rich.console import Console
from rich.table import Table
from App.controllers import get_exams,detect_exam_clash,create_exam,parse_date,parse_time,get_course,get_courses
from flask import current_app
from .utils import date_checker,time_checker,course_checker,setting_checker,rule_set_handler,rule_set

console = Console()
exam = AppGroup("exam", help="Commands that relate to the management of examinations with all commands having a customisable rule setting")


@exam.command("list", help="[RULE_SETTING] #list existing exams")
def ls():
    console.print("\n")
    rule_setting = setting_checker(None,None,click.prompt("Rule Setting", default="all", type=click.Choice(["1", "2", "all", "none"], case_sensitive=False), show_default=True, show_choices=True))
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

@exam.command("clashes", help="[RULE_SETTING] #list clashes")
def clashes():
    console.print("\n")
    rule_setting = setting_checker(None,None,click.prompt("Rule Setting", default="all", type=click.Choice(["1", "2", "all", "none"], case_sensitive=False), show_default=True, show_choices=True))
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

@exam.command("schedule", help="[COURSE_CODE] [DATE] [START_TIME] [END_TIME] [RULE_SETTING] #schedule an exam")
def schedule():
    console.print("\n")
    course_code = course_checker(None,None,click.prompt("Course Code", default="COMP1700", show_default=True))
    date = date_checker(None,None,click.prompt("Exam Date", default="2024-12-06", show_default=True))
    start_time = time_checker(None,None,click.prompt("Exam Start Time", default="08:00", show_default=True))
    end_time = time_checker(None,None,click.prompt("Exam End Time", default="10:00", show_default=True))
    rule_setting = setting_checker(None,None,click.prompt("Rule Setting", default="all", type=click.Choice(["1", "2", "all", "none"], case_sensitive=False), show_default=True, show_choices=True))

    rule_set_handler(rule_setting)

    date = parse_date(date)
    start_time = parse_time(start_time)
    end_time = parse_time(end_time)
    exam = create_exam(course_code, date, start_time, end_time)
    if detect_exam_clash(exam,rule_set[0],rule_set[1]):
        console.print("[red]ERROR! Clash Detected!")
    else:
        console.print(f"[green]Exam for {course_code} scheduled on {date} from {start_time} to {end_time}")
    console.print("\n")