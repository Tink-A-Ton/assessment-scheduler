import click
from flask.cli import AppGroup
from rich.console import Console
from rich.table import Table
from App.controllers import get_exams,get_clashes

console = Console()
exam = AppGroup("exam", help="Commands that relate to the management of examinations")

@exam.command("ls", help="This command shows the list of all existing exams")
def ls():
    console.print("\n")
    results = get_exams()
    table = Table(title="Existing Examinations")
    table.add_column("Course Code", style="yellow")
    table.add_column("Start Date", style="magenta")
    table.add_column("Start Time", style="magenta")
    table.add_column("End Time", style="magenta")
    table.add_column("Clash?", style="cyan")
    for result in results:
        table.add_row(result.course_code, str(result.start_date), str(result.start_time), str(result.end_time), str(result.clash_detected))
    console.print(table)
    console.print("\n")

@exam.command("clashes", help="This command shows the list of all CLASHING exams")
def clashes():
    console.print("\n")
    results = get_clashes()
    table = Table(title="Clashing Examinations")
    table.add_column("Course Code", style="yellow")
    table.add_column("Start Date", style="magenta")
    table.add_column("Start Time", style="magenta")
    table.add_column("End Time", style="magenta")
    table.add_column("Clash?", style="cyan")
    for result in results:
        table.add_row(result.course_code, str(result.start_date), str(result.start_time), str(result.end_time), str(result.clash_detected))
    console.print(table)
    console.print("\n")