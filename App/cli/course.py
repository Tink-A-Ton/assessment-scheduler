import click
from flask.cli import AppGroup
from rich.console import Console
from rich.table import Table
from App.controllers import get_courses,create_course

console = Console()
course = AppGroup("course", help="Commands that relate to the management of courses")

@course.command("create", help="This command creates a course")
@click.argument("course_code")
@click.argument("course_title")
@click.argument("level", default=1)
@click.argument("semester", default=1)
def assign_course(course_code, course_title, level, semester):
    console.print("\n")
    level = int(level)
    semester = int(semester)
    if create_course(course_code, course_title, level, semester):
        console.print("[green]Course added successfully")
    else:
        console.print("[red]Failed to add Course")
    console.print("\n")

@course.command("ls", help="This command shows the list of all existing courses")
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