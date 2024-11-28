from App.database import db
from App.models import (
    Course,
    Staff,
    Admin,
    Semester,
    CourseInstructor,
    Programme,
    CourseProgramme
)
from App.models.courseAssessment import CourseAssessment
from datetime import datetime, date, time


def initialize() -> None:
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
    staff = Staff(
        first_name="Jane",
        last_name="Doe",
        id=11111111,
        email="jane@mail.com",
        position="Part-Time Tutor",
        password="password",
    )
    db.session.add(staff)

    # assign staff to courses
    cs1 = CourseInstructor(staff_id=11111111, course_code="COMP1700")
    cs2 = CourseInstructor(staff_id=11111111, course_code="COMP2700")
    cs3 = CourseInstructor(staff_id=11111111, course_code="COMP3700")
    db.session.add(cs1)
    db.session.add(cs2)
    db.session.add(cs3)

    ca1 = CourseAssessment(
        course_code="COMP1700",
        start_date=parse_date("2024-11-08"),
        end_date=parse_date("2024-11-08"),
        start_time=parse_time("08:00"),
        end_time=parse_time("10:00"),
        clash_detected=False,
    )
    ca2 = CourseAssessment(
        course_code="COMP1700",
        start_date=parse_date("2024-11-09"),
        end_date=parse_date("2024-11-09"),
        start_time=parse_time("00:00"),
        end_time=parse_time("23:59"),
        clash_detected=False,
    )
    ca3 = CourseAssessment(
        course_code="COMP1700",
        start_date=parse_date("2024-11-10"),
        end_date=parse_date("2024-11-10"),
        start_time=parse_time("09:00"),
        end_time=parse_time("12:00"),
        clash_detected=False,
    )
    ca4 = CourseAssessment(
        course_code="COMP2700",
        start_date=parse_date("2024-11-15"),
        end_date=parse_date("2024-11-15"),
        start_time=parse_time("08:00"),
        end_time=parse_time("10:00"),
        clash_detected=False,
    )
    ca5 = CourseAssessment(
        course_code="COMP2700",
        start_date=parse_date("2024-11-16"),
        end_date=parse_date("2024-11-16"),
        start_time=parse_time("00:00"),
        end_time=parse_time("23:59"),
        clash_detected=False,
    )
    ca6 = CourseAssessment(
        course_code="COMP2700",
        start_date=parse_date("2024-11-17"),
        end_date=parse_date("2024-11-17"),
        start_time=parse_time("09:00"),
        end_time=parse_time("12:00"),
        clash_detected=False,
    )
    ca7 = CourseAssessment(
        course_code="COMP3700",
        start_date=parse_date("2024-11-22"),
        end_date=parse_date("2024-11-22"),
        start_time=parse_time("08:00"),
        end_time=parse_time("10:00"),
        clash_detected=False,
    )
    ca8 = CourseAssessment(
        course_code="COMP3700",
        start_date=parse_date("2024-11-23"),
        end_date=parse_date("2024-11-23"),
        start_time=parse_time("00:00"),
        end_time=parse_time("23:59"),
        clash_detected=False,
    )
    ca9 = CourseAssessment(
        course_code="COMP3700",
        start_date=parse_date("2024-11-24"),
        end_date=parse_date("2024-11-24"),
        start_time=parse_time("09:00"),
        end_time=parse_time("12:00"),
        clash_detected=False,
    )
    ca10 = CourseAssessment(
        course_code="COMP1701",
        start_date=parse_date("2024-11-25"),
        end_date=parse_date("2024-11-25"),
        start_time=parse_time("08:00"),
        end_time=parse_time("09:00"),
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
    db.session.add(ca10)
    
    p1 = Programme(name="BSc. Computer Science (General)")
    p2 = Programme(name="BSc. Computer Science (Special)")
    p3 = Programme(name="BSc. Computer Science and Management")
    p4 = Programme(name="BSc. Information Technology (General)")
    p5 = Programme(name="BSc. Information Technology (Special)")
    db.session.add_all([p1, p2, p3, p4, p5])
    db.session.flush()

    course_programmes = [
        CourseProgramme(course_code="COMP1700", programme_id=p1.id),
        CourseProgramme(course_code="COMP1700", programme_id=p2.id),
        CourseProgramme(course_code="COMP1701", programme_id=p1.id),
        CourseProgramme(course_code="COMP1701", programme_id=p4.id),
        CourseProgramme(course_code="COMP2700", programme_id=p1.id),
        CourseProgramme(course_code="COMP2700", programme_id=p3.id),
        CourseProgramme(course_code="COMP2701", programme_id=p2.id),
        CourseProgramme(course_code="COMP3700", programme_id=p5.id),
        CourseProgramme(course_code="COMP3701", programme_id=p5.id),
    ]
    db.session.add_all(course_programmes)

    db.session.commit()


# Helper function to parse date and time strings
def parse_date(date_str):
    if date_str == "":
        return datetime.now().date()
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def parse_time(time_str):
    if time_str == "":
        return datetime.now().time()
    time_str = time_str[:5]
    return datetime.strptime(time_str, "%H:%M").time()
