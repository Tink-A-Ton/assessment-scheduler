import click
from flask.cli import AppGroup
from rich.console import Console
from rich.table import Table
from App.controllers import get_courses,create_course,get_course
from flask import current_app
from .utils import course_not_exist_checker

console = Console()
course = AppGroup("course", help="Commands that relate to the management of courses")


@course.command("create", help="[COURSE_CODE] [COURSE_TITLE] [LEVEL] [SEMESTER] #creates a course")
def assign_course():
    console.print("\n")
    course_code = course_not_exist_checker(None,None,click.prompt("Course Code", default="COMP1605", show_default=True))
    course_title = click.prompt("course_title", default="Computer Fantasy", show_default=True)
    level = click.prompt("level", default=1, show_default=True)
    semester = click.prompt("semester", default=1, show_default=True)
    level = int(level)
    semester = int(semester)
    if create_course(course_code, course_title, level, semester):
        console.print(f"[green]Course with code {course_code} added successfully")
    else:
        console.print(f"[red]Failed to add Course with code {course_code}")
    console.print("\n")

@course.command("list", help="This command shows the list of all existing courses")
def ls():
    console.print("\n")
    courses = get_courses()
    table = Table(title="Existing Courses")
    table.add_column("Course Code", style="yellow")
    table.add_column("Course Title", style="cyan")
    table.add_column("Semester ID", style="cyan")
    table.add_column("Level", style="cyan")
    for c in courses:
        table.add_row(str(c.course_code), c.course_title, str(c.semester_id), str(c.level))
    console.print(table)
    console.print("\n")