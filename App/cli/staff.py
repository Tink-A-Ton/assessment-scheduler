import click
from flask.cli import AppGroup
from rich.console import Console
from rich.table import Table
from App.controllers import get_all_staff,get_staff,get_staff_courses,get_staff_exams,detect_exam_clash,get_exam
from App.models import Exam
from flask import current_app
from .utils import setting_checker,rule_set_handler,staff_id_checker,rule_set

console = Console()
staff = AppGroup("staff", help="Commands that relate to the management of staff members")


@staff.command("list", help="This command shows the list of all existing courses")
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
def lookup():
    console.print("\n")
    id = staff_id_checker(None,None,click.prompt("Staff ID", default="11111111", show_default=True))
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
def courses():
    console.print("\n")
    id = staff_id_checker(None,None,click.prompt("Staff ID", default="11111111", show_default=True))
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
def exams():
    console.print("\n")
    id = staff_id_checker(None,None,click.prompt("Staff ID", default="11111111", show_default=True))
    rule_setting = setting_checker(None,None,click.prompt("rule_setting", default="all", type=click.Choice(["1", "2", "all", "none"], case_sensitive=False), show_default=True, show_choices=True))
    staff_member = get_staff(int(id))

    rule_set_handler(rule_setting)

    if staff_member:
        results = get_staff_exams(int(id))
        table = Table(title=f"Scheduled Examinations of {staff_member.first_name} {staff_member.last_name}")
        table.add_column("Course Code", style="yellow")
        table.add_column("Start Date", style="magenta")
        table.add_column("Start Time", style="magenta")
        table.add_column("End Time", style="magenta")
        table.add_column("Clash?", style="cyan")
        for result in results:
            temp = get_exam(int(result['id'])) #will never return "None" we assume
            detect_exam_clash(temp,rule_set[0],rule_set[1])
            result = temp.to_json() # type: ignore
            table.add_row(result.get("course_code"), str(result.get("start_date")), str(result.get("start_time")), str(result.get("end_time")), str(result.get("clash_detected")))
        console.print(table)
    else:
        console.print(f"[red]Staff member with id {id} does not exist")
    console.print("\n")

# @staff.command("clashes", help="[ID] #shows clashes from specified staff member")
# @click.argument("id", default="11111111", callback=staff_id_checker)
# @click.argument("rule_setting", default="all", callback=setting_checker, type=click.Choice(["1", "2", "all", "none"], case_sensitive=False))
# def clashes(id):
@staff.command("clashes", help="[ID] #shows clashes from specified staff member")
def clashes():
    console.print("\n")
    id = staff_id_checker(None,None,click.prompt("id", default="11111111", show_default=True))
    rule_setting = setting_checker(None,None,click.prompt("rule_setting", default="all", type=click.Choice(["1", "2", "all", "none"], case_sensitive=False), show_default=True, show_choices=True))
    staff_member = get_staff(int(id))

    rule_set_handler(rule_setting)

    if staff_member:
        results = get_staff_exams(int(id))
        table = Table(title=f"Clashing Examinations of {staff_member.first_name} {staff_member.last_name}")
        table.add_column("Course Code", style="yellow")
        table.add_column("Start Date", style="magenta")
        table.add_column("Start Time", style="magenta")
        table.add_column("End Time", style="magenta")
        table.add_column("Clash?", style="cyan")
        for result in results:
            temp = get_exam(int(result['id'])) #will never return "None" we assume
            detect_exam_clash(temp,rule_set[0],rule_set[1])
            result = temp.to_json() # type: ignore
            if result.get("clash_detected"):
                table.add_row(result.get("course_code"), str(result.get("start_date")), str(result.get("start_time")), str(result.get("end_time")), str(result.get("clash_detected")))
        console.print(table)
    else:
        console.print(f"[red]Staff member with id {id} does not exist")
    console.print("\n")