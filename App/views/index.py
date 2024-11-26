from flask import Blueprint, request, jsonify, render_template
from App.database import db
from App.models import (
    Staff,
    Course,
    Assessment,
    Programme,
    Admin,
    Semester,
    CourseInstructor,
    Assessment,
)
from App.models.courseAssessment import CourseAssessment

index_views = Blueprint("index_views", __name__, template_folder="../templates")


@index_views.route("/", methods=["GET"])
def index():
    return render_template("login.html")


@index_views.route("/init", methods=["GET"])
def init():
    db.drop_all()
    db.create_all()
    bob = Admin(999, "bob@mail.com", "bobpass")
    db.session.add(bob)
    sem = Semester(
        start_date="01-02-2024",
        end_date="01-05-2024",
        semester_number=1,
        max_assessments=3,
    )
    db.session.add(sem)

    # create courses
    c1 = Course(
        course_code="COMP1700",
        course_title="Introduction to C++",
        # description="C++ basics",
        level=1,
        semester_id=1,
        # aNum=3,
    )
    c2 = Course(
        course_code="COMP1701",
        course_title="Introduction to Web Development",
        # description="Web development basics",
        level=1,
        semester_id=1,
        # aNum=3,
    )
    c3 = Course(
        course_code="COMP2700",
        course_title="Advanced C++",
        # description="Advanced C++",
        level=2,
        semester_id=1,
        # aNum=3,
    )
    c4 = Course(
        course_code="COMP2701",
        course_title="Advanced Web Development",
        # description="Advanced web development",
        level=2,
        semester_id=1,
        # aNum=3,
    )
    c5 = Course(
        course_code="COMP3700",
        course_title="Data Science Fundamentals",
        # description="Introduction to python and datasets",
        level=3,
        semester_id=1,
        # aNum=3,
    )
    c6 = Course(
        course_code="COMP3701",
        course_title="Advanced Data Science",
        # description="Analyzing Big Data with Python",
        level=3,
        semester_id=1,
        # aNum=3,
    )
    db.session.add(c1)
    db.session.add(c2)
    db.session.add(c3)
    db.session.add(c4)
    db.session.add(c5)
    db.session.add(c6)

    # create staff
    # staff = create_staff()
    # staff = Staff.register(
    #     firstName="Jane",
    #     lastName="Doe",
    #     u_ID=11111111,
    #     status="Lecturer",
    #     email="jane@mail.com",
    #     password="password",
    # )

    # assign staff to courses
    cs1 = CourseInstructor(staff_id=11111111, course_code="COMP1700")
    cs2 = CourseInstructor(staff_id=11111111, course_code="COMP2700")
    cs3 = CourseInstructor(staff_id=11111111, course_code="COMP3700")
    db.session.add(cs1)
    db.session.add(cs2)
    db.session.add(cs3)

    # create assessments
    asm1 = Assessment(category="EXAM")
    db.session.add(asm1)
    asm2 = Assessment(category="ASSIGNMENT")
    db.session.add(asm2)
    asm3 = Assessment(category="QUIZ")
    db.session.add(asm3)
    asm4 = Assessment(category="PROJECT")
    db.session.add(asm4)
    asm5 = Assessment(category="DEBATE")
    db.session.add(asm5)
    asm6 = Assessment(category="PRESENTATION")
    db.session.add(asm6)
    asm7 = Assessment(category="ORALEXAM")
    db.session.add(asm7)
    asm8 = Assessment(category="PARTICIPATION")
    db.session.add(asm8)

    # create course assessments
    from datetime import datetime, date, time

    # Helper function to parse date and time strings
    def parse_date(date_str) -> date:
        return datetime.strptime(date_str, "%Y-%m-%d").date()

    def parse_time(time_str) -> time:
        return datetime.strptime(time_str, "%H:%M:%S").time()

    ca1 = CourseAssessment(
        course_code="COMP1700",
        assessment_id=1,
        start_date=parse_date("2024-04-08"),
        end_date=parse_date("2024-04-08"),
        start_time=parse_time("08:00:00"),
        end_time=parse_time("10:00:00"),
        clash_detected=False,
    )
    ca2 = CourseAssessment(
        course_code="COMP1700",
        assessment_id=3,
        start_date=parse_date("2024-04-09"),
        end_date=parse_date("2024-04-09"),
        start_time=parse_time("00:00:00"),
        end_time=parse_time("23:59:00"),
        clash_detected=False,
    )
    ca3 = CourseAssessment(
        course_code="COMP1700",
        assessment_id=6,
        start_date=parse_date("2024-04-10"),
        end_date=parse_date("2024-04-10"),
        start_time=parse_time("09:00:00"),
        end_time=parse_time("12:00:00"),
        clash_detected=False,
    )
    ca4 = CourseAssessment(
        course_code="COMP2700",
        assessment_id=1,
        start_date=parse_date("2024-04-15"),
        end_date=parse_date("2024-04-15"),
        start_time=parse_time("08:00:00"),
        end_time=parse_time("10:00:00"),
        clash_detected=False,
    )
    ca5 = CourseAssessment(
        course_code="COMP2700",
        assessment_id=3,
        start_date=parse_date("2024-04-16"),
        end_date=parse_date("2024-04-16"),
        start_time=parse_time("00:00:00"),
        end_time=parse_time("23:59:00"),
        clash_detected=False,
    )
    ca6 = CourseAssessment(
        course_code="COMP2700",
        assessment_id=6,
        start_date=parse_date("2024-04-17"),
        end_date=parse_date("2024-04-17"),
        start_time=parse_time("09:00:00"),
        end_time=parse_time("12:00:00"),
        clash_detected=False,
    )
    ca7 = CourseAssessment(
        course_code="COMP3700",
        assessment_id=1,
        start_date=parse_date("2024-04-22"),
        end_date=parse_date("2024-04-22"),
        start_time=parse_time("08:00:00"),
        end_time=parse_time("10:00:00"),
        clash_detected=False,
    )
    ca8 = CourseAssessment(
        course_code="COMP3700",
        assessment_id=3,
        start_date=parse_date("2024-04-23"),
        end_date=parse_date("2024-04-23"),
        start_time=parse_time("00:00:00"),
        end_time=parse_time("23:59:00"),
        clash_detected=False,
    )
    ca9 = CourseAssessment(
        course_code="COMP3700",
        assessment_id=6,
        start_date=parse_date("2024-04-24"),
        end_date=parse_date("2024-04-24"),
        start_time=parse_time("09:00:00"),
        end_time=parse_time("12:00:00"),
        clash_detected=False,
    )

    db.session.add(ca1)
    db.session.add(ca2)
    db.session.add(ca3)
    db.session.add(ca4)
    db.session.add(ca5)
    db.session.add(ca6)
    db.session.add(ca7)
    db.session.add(ca8)
    db.session.add(ca9)

    db.session.commit()
    return {"message": "Objects created"}
