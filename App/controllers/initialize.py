import csv
from ..database import db
from ..models import (
    Semester,
    Programme,
    ProgrammeCourse,
    Exam,
)
from .admin import create_admin
from .semester import create_semester, get_semester
from .staff import create_staff, add_instructor
from .course import create_course
from .exam import create_exam
from .clash import detect_exam_clash
from App.models.utils import parse_date, parse_time


def initialize() -> None:
    db.drop_all()
    db.create_all()

    with open("App/uploads/admin.csv") as admin_file:
        reader = csv.DictReader(admin_file)
        for row in reader:
            create_admin(int(row["id"]), row["email"], row["password"])

    with open("App/uploads/staff.csv") as staff_file:
        reader = csv.DictReader(staff_file)
        for row in reader:
            create_staff(
                int(row["id"]),
                row["email"],
                row["password"],
                row["first_name"],
                row["last_name"],
                row["position"],
            )

    with open("App/uploads/semester.csv") as semester_file:
        reader = csv.DictReader(semester_file)
        for row in reader:
            create_semester(
                row["start_date"],
                row["end_date"],
                int(row["semester_number"]),
                int(row["max_exams"]),
            )

    with open("App/uploads/courses.csv") as courses_file:
        reader = csv.DictReader(courses_file)
        semester: Semester = get_semester()
        for row in reader:
            create_course(
                row["course_code"], row["title"], int(row["level"]), semester.id
            )

    with open("App/uploads/instructors.csv") as instructors_file:
        reader = csv.DictReader(instructors_file)
        for row in reader:
            add_instructor(int(row["staff_id"]), row["course_code"])

    with open("App/uploads/programmes.csv") as programmes_file:
        reader = csv.DictReader(programmes_file)
        for row in reader:
            add_programme(row["name"])

    with open("App/uploads/programme_courses.csv") as programme_courses_file:
        reader = csv.DictReader(programme_courses_file)
        for row in reader:
            add_programme_course(int(row["programme_id"]), row["course_code"])

    with open("App/uploads/exams.csv") as exams_file:
        reader = csv.DictReader(exams_file)
        for row in reader:
            exam: Exam = create_exam(
                row["course_code"],
                parse_date(row["start_date"]),
                parse_time(row["start_time"]),
                parse_time(row["end_time"]),
            )
            detect_exam_clash(exam, "rule1", "rule2")


def add_programme(programme_title: str):
    programme: Programme = Programme(programme_title)
    db.session.add(programme)
    db.session.commit()


def add_programme_course(programme_id: int, course_code: str):
    programme_course: ProgrammeCourse = ProgrammeCourse(course_code, programme_id)
    db.session.add(programme_course)
    db.session.commit()
