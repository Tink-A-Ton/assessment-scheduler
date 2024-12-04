import click
from flask.cli import AppGroup
from rich.console import Console
from rich.table import Table
from App.controllers import get_all_staff,get_staff,get_staff_courses,get_staff_exams
from flask import current_app

console = Console()
staff = AppGroup("staff", help="Commands that relate to the management of staff members")


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


@staff.command("ls", help="This command shows the list of all existing courses")
def ls():
    staff = get_all_staff()
    table = Table(title="Staff Members")
    table.add_column("id", style="yellow")
    table.add_column("First Name", style="cyan")
    table.add_column("Last Name", style="cyan")
    table.add_column("Position", style="cyan")
    for s in staff:
        table.add_row(str(s.id), s.first_name, s.last_name, s.position.value)
    console.print(table)

@staff.command("lookup", help="[ID] #display specified staff member")
@click.argument("id", default="11111111", callback=staff_id_checker)
def lookup(id):
    console.print("\n")
    staff_member = get_staff(int(id))
    if not staff_member:
        console.print("Staff member with the id "+str(id)+" does not exist")
    else:
        console.print(f"[yellow]ID: [cyan]{staff_member.id}")
        console.print(f"[yellow]First Name: [cyan]{staff_member.first_name}")
        console.print(f"[yellow]Last Name: [cyan]{staff_member.last_name}")
        console.print(f"[yellow]Position: [cyan]{staff_member.position.value}")
    console.print("\n")

@staff.command("courses", help="[ID] #shows courses a staff member is responsible for")
@click.argument("id", default="11111111", callback=staff_id_checker)
def courses(id):
    console.print("\n")
    staff_member = get_staff(int(id))
    if staff_member:
        results = get_staff_courses(int(id))
        table = Table(title=f"Registered Courses of {staff_member.first_name} {staff_member.last_name}")
        table.add_column("Course Code", style="yellow")
        table.add_column("Course Title", style="cyan")
        table.add_column("Semester ID", style="cyan")
        table.add_column("Level", style="cyan")
        for result in results:
            table.add_row(result.get("course_code"), result.get("course_title"), str(result.get("semester_id")), str(result.get("level")))
        console.print(table)
    else:
        console.print(f"[red]Staff member with id {id} does not exist")
    console.print("\n")


@staff.command("exams", help="[ID] #shows exams from specified staff member")
@click.argument("id", default="11111111", callback=staff_id_checker)
def exams(id):
    console.print("\n")
    staff_member = get_staff(int(id))
    if staff_member:
        results = get_staff_exams(int(id))
        table = Table(title=f"Scheduled Examinations of {staff_member.first_name} {staff_member.last_name}")
        table.add_column("Course Code", style="yellow")
        table.add_column("Start Date", style="magenta")
        table.add_column("Start Time", style="magenta")
        table.add_column("End Time", style="magenta")
        table.add_column("Clash?", style="cyan")
        for result in results:
            table.add_row(result.get("course_code"), str(result.get("start_date")), str(result.get("start_time")), str(result.get("end_time")), str(result.get("clash_detected")))
        console.print(table)
    else:
        console.print(f"[red]Staff member with id {id} does not exist")
    console.print("\n")

@staff.command("clashes", help="[ID] #shows clashes from specified staff member")
@click.argument("id", default="11111111", callback=staff_id_checker)
def clashes(id):
    console.print("\n")
    staff_member = get_staff(int(id))
    if staff_member:
        results = get_staff_exams(int(id))
        table = Table(title=f"Clashing Examinations of {staff_member.first_name} {staff_member.last_name}")
        table.add_column("Course Code", style="yellow")
        table.add_column("Start Date", style="magenta")
        table.add_column("Start Time", style="magenta")
        table.add_column("End Time", style="magenta")
        table.add_column("Clash?", style="cyan")
        for result in results:
            if result.get("clash_detected"):
                table.add_row(result.get("course_code"), str(result.get("start_date")), str(result.get("start_time")), str(result.get("end_time")), str(result.get("clash_detected")))
        console.print(table)
    else:
        console.print(f"[red]Staff member with id {id} does not exist")
    console.print("\n")