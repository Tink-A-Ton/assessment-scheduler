import click, sys, csv
from flask import Flask
from flask.cli import with_appcontext, AppGroup
from flask_migrate import Migrate
from App.database import db, get_migrate
from App.main import create_app
from App.models import Staff, Course, Programme, Admin
from App.controllers.initialize import initialize
from App.controllers.course import create_course
from rich.console import Console
from rich.table import Table

# This commands file allow you to create convenient CLI commands for testing controllers!!
app: Flask = create_app()
migrate: Migrate = get_migrate(app)
console = Console()


# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init() -> None:
    initialize()
    print("database initialized")


# This command retrieves all staff objects
@app.cli.command("get-users")
def get_users():
    staff = Staff.query.all()
    table = Table(title="Staff Members")
    table.add_column("id", style="yellow")
    table.add_column("First Name", style="cyan")
    table.add_column("Last Name", style="cyan")
    table.add_column("Position", style="cyan")
    for s in staff:
        table.add_row(str(s.id), s.first_name, s.last_name, s.position.value)
    console.print(table)

    # This command creates all the Exam objects
    # @app.cli.command("asm")
    # def load_Asm():
    #   db.create_all()
    #   asm1 = Exam(category='EXAM')
    #   db.session.add(asm1)
    #   db.session.commit()

    #   asm2 = Exam(category='ASSIGNMENT')
    #   db.session.add(asm2)
    #   db.session.commit()

    #   asm3 = Exam(category='QUIZ')
    #   db.session.add(asm3)
    #   db.session.commit()

    #   asm4 = Exam(category='PROJECT')
    #   db.session.add(asm4)
    #   db.session.commit()

    #   asm5 = Exam(category='DEBATE')
    #   db.session.add(asm5)
    #   db.session.commit()

    #   asm6 = Exam(category='PRESENTATION')
    #   db.session.add(asm6)
    #   db.session.commit()

    #   asm7 = Exam(category='ORALEXAM')
    #   db.session.add(asm7)
    #   db.session.commit()

    #   asm8 = Exam(category='PARTICIPATION')
    #   db.session.add(asm8)
    #   db.session.commit()

    # # This command creates all the Programme objects
    # @app.cli.command("pgr")
    # def load_Pgr():
    #   db.create_all()
    #   pgr1 = Programme(p_name='Computer Science Major')
    #   db.session.add(pgr1)
    #   db.session.commit()

    #   pgr2 = Programme(p_name='Computer Science Minor')
    #   db.session.add(pgr2)
    #   db.session.commit()

    #   pgr3 = Programme(p_name='Computer Science Special')
    #   db.session.add(pgr3)
    #   db.session.commit()

    #   pgr4 = Programme(p_name='Information Technology Major')
    #   db.session.add(pgr4)
    #   db.session.commit()

    #   pgr5 = Programme(p_name='Information Technology Minor')
    #   db.session.add(pgr5)
    #   db.session.commit()

    #   pgr6 = Programme(p_name='Information Technology Special')
    #   db.session.add(pgr6)
    #   db.session.commit()

    print("All programmes added")


# This command assigns courses to staff
@app.cli.command("add-course")
@click.argument("course_code")
@click.argument("course_title")
@click.argument("level", default=1)
@click.argument("semester", default=1)
def assign_course(course_code, course_title, level, semester):
    level = int(level)
    semester = int(semester)
    if create_course(course_code, course_title, level, semester):
        console.print("[green]Course added successfully")
    else:
        console.print("[red]Failed to add Course")

    

    


# load course data from csv file
# @app.cli.command("load-courses")
# def load_course_data():
# with open('courses.csv') as file: #csv files are used for spreadsheets
#   reader = csv.DictReader(file)
#   for row in reader:
#     new_course = Course(courseCode=row['courseCode'], courseTitle=row['courseTitle'], description=row['description'],
#       level=row['level'], semester=row['semester'], preReqs=row['preReqs'], p_ID=row['p_ID'],)  #create object
#     db.session.add(new_course)
#   db.session.commit() #save all changes OUTSIDE the loop
# print('database intialized')
