import click, sys, csv
from flask import Flask
from flask.cli import with_appcontext, AppGroup
from flask_migrate import Migrate
from App.database import db, get_migrate
from App.main import create_app
from App.models import Staff, Course, Programme, Admin
from App.controllers.initialize import initialize
from App.controllers.course import create_course
from App.cli import course,exam,staff

# This commands file allow you to create convenient CLI commands for testing controllers!!
app: Flask = create_app()
migrate: Migrate = get_migrate(app)


# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init() -> None:
    initialize()
    print("database initialized")

# Utilise CLI defined in App/cli
app.cli.add_command(staff)
app.cli.add_command(course)
app.cli.add_command(exam)


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
