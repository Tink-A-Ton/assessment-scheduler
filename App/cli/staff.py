import click
from flask.cli import AppGroup
from rich.console import Console
from rich.table import Table
from App.controllers import (
    get_all_staff,
    get_staff,
    get_staff_courses,
    get_staff_exams,
    detect_exam_clash,
    get_exam,
)
from App.models import Exam
from flask import current_app
from .utils import (
    setting_checker,
    rule_set_handler,
    staff_id_checker,
    rule_set,
    rule_setting_prompt,
)

console = Console()
staff = AppGroup("staff", help="Commands that relate to the management of staff members")


@staff.command("list", help="Lists all existing staff members")
def list_staff():
    staff = get_all_staff()
    table = Table(title="Staff Members")
    table.add_column("id", style="yellow")
    table.add_column("First Name", style="cyan")
    table.add_column("Last Name", style="cyan")
    table.add_column("Position", style="cyan")
    for s in staff:
        table.add_row(str(s.id), s.first_name, s.last_name, s.position)
    console.print(table)


@staff.command("lookup", help="Displays specified staff member")
def lookup():
    console.print("\n")
    id = staff_id_checker(
        None, None, click.prompt("Staff ID", default="900000003", show_default=True)
    )
    staff_member = get_staff(int(id))
    if not staff_member:
        console.print("Staff member with the id " + str(id) + " does not exist")
    else:
        console.print(f"[yellow]ID: [cyan]{staff_member.id}")
        console.print(f"[yellow]First Name: [cyan]{staff_member.first_name}")
        console.print(f"[yellow]Last Name: [cyan]{staff_member.last_name}")
        console.print(f"[yellow]Position: [cyan]{staff_member.position}")
    console.print("\n")


@staff.command(
    "courses", help="Shows courses that a specified staff member is responsible for"
)
def courses():
    console.print("\n")
    id = staff_id_checker(
        None, None, click.prompt("Staff ID", default="900000003", show_default=True)
    )
    staff_member = get_staff(int(id))
    if staff_member:
        results = get_staff_courses(int(id))
        table = Table(
            title=f"Registered Courses of {staff_member.first_name} {staff_member.last_name}"
        )
        table.add_column("Course Code", style="yellow")
        table.add_column("Course Title", style="cyan")
        table.add_column("Semester ID", style="cyan")
        table.add_column("Level", style="cyan")
        for result in results:
            table.add_row(
                result.get("course_code"),
                result.get("course_title"),
                str(result.get("semester_id")),
                str(result.get("level")),
            )
        console.print(table)
    else:
        console.print(f"[red]Staff member with id {id} does not exist")
    console.print("\n")


@staff.command(
    "exams", help="Shows exams that a specified staff member is responsible for"
)
def exams():
    console.print("\n")
    id = staff_id_checker(
        None, None, click.prompt("Staff ID", default="900000003", show_default=True)
    )
    rule_setting_prompt()
    staff_member = get_staff(int(id))
    if staff_member:
        results = get_staff_exams(int(id))
        table = Table(
            title=f"Scheduled Examinations of {staff_member.first_name} {staff_member.last_name}"
        )
        table.add_column("Course Code", style="yellow")
        table.add_column("Start Date", style="magenta")
        table.add_column("Start Time", style="magenta")
        table.add_column("End Time", style="magenta")
        table.add_column("Clash?", style="cyan")
        for result in results:
            temp: Exam| None = get_exam(int(result["id"]))  # will never return "None" we assume
            if temp is None:
                return
            detect_exam_clash(temp, rule_set[0], rule_set[1])
            result = temp.to_json()  
            table.add_row(
                result.get("course_code"),
                str(result.get("start_date")),
                str(result.get("start_time")),
                str(result.get("end_time")),
                str(result.get("clash_detected")),
            )
        console.print(table)
    else:
        console.print(f"[red]Staff member with id {id} does not exist")
    console.print("\n")


@staff.command(
    "clashes", help="Shows clashes that a specified staff member is responsible for"
)
def clashes():
    console.print("\n")
    id = staff_id_checker(
        None, None, click.prompt("id", default="900000003", show_default=True)
    )
    rule_setting_prompt()
    staff_member = get_staff(int(id))
    if staff_member:
        exams = get_staff_exams(int(id))
        table = Table(
            title=f"Clashing Examinations of {staff_member.first_name} {staff_member.last_name}"
        )
        table.add_column("Course Code", style="yellow")
        table.add_column("Start Date", style="magenta")
        table.add_column("Start Time", style="magenta")
        table.add_column("End Time", style="magenta")
        table.add_column("Clash?", style="cyan")
        for exam in exams:
            temp = get_exam(int(exam["id"]))  # will never return "None" we assume
            detect_exam_clash(temp, rule_set[0], rule_set[1])
            if temp is None:
                return
            exam = temp.to_json()  # type: ignore
            if exam.get("clash_detected"):
                table.add_row(
                    exam.get("course_code"),
                    str(exam.get("start_date")),
                    str(exam.get("start_time")),
                    str(exam.get("end_time")),
                    str(exam.get("clash_detected")),
                )
        console.print(table)
    else:
        console.print(f"[red]Staff member with id {id} does not exist")
    console.print("\n")
