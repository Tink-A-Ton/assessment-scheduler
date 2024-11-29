from flask import (
    Blueprint,
    request,
    jsonify,
    render_template,
    redirect,
    url_for,
    flash,
    get_flashed_messages,
    session,
)
from flask import current_app as app
from flask_mail import Mail, Message
from werkzeug import Response
from App.database import db
import json
from flask_jwt_extended import current_user as jwt_current_user, get_jwt_identity
from flask_jwt_extended import jwt_required
from datetime import date, time, timedelta
import time
from ..models import Course, Exam, Staff, Semester
from App.controllers.staff import (
    get_registered_courses,
    create_staff,
    add_instructor,
    get_staff,
)
from App.controllers.course import get_all_courses, get_courses_by_level
from App.controllers.exam import (
    get_exam,
    get_exams_by_course,
    create_exam,
    delete_exam,
    get_exams,
)
from App.controllers.initialize import parse_date, parse_time
from App.models import User, Staff, ClashContext

staff_views = Blueprint("staff_views", __name__, template_folder="../templates")


# Gets Signup Page
@staff_views.route("/signup", methods=["GET"])
def get_signup_page():
    return render_template("signup.html")


# Gets Calendar Page
@staff_views.route("/calendar", methods=["GET"])
@jwt_required()
def get_calendar_page():
    staff: Staff = get_staff(get_jwt_identity())

    all_courses: list[Course] = get_all_courses()
    registered_courses: list[Course] = get_registered_courses(staff.id)
    other_courses: list[Course] = [
        course for course in all_courses if course not in registered_courses
    ]
    staff_courses: list[dict] = [course.to_json() for course in registered_courses]
    staff_exams: list[dict] = [
        assessment.to_json()
        for course in registered_courses
        for assessment in get_exams_by_course(course.course_code)
    ]

    other_exams: list[dict] = [
        assessment.to_json() for assessment in get_exams()
    ]
    semester: Semester = Semester.query.order_by(Semester.id.desc()).first()
    semester_details: dict[str, str] = {
        "start": semester.start_date,
        "end": semester.end_date,
    }

    messages = []
    if "message" in session:
        messages.append(session.pop("message"))

    return render_template(
        "index.html",
        courses=other_courses,
        staff_courses=staff_courses,
        staff_exams=staff_exams,
        semester=semester_details,
        other_exams=other_exams,
        messages=messages,
    )


@staff_views.route("/calendar", methods=["POST"])
@jwt_required()
def update_calendar_page():
    data = request.form

    if data is None:
        return redirect(url_for("staff_views.get_calendar_page"))

    id: int = int(data["id"]) if "id" in data else 0  # patch fix  very very verybad

    startDate: date = parse_date(request.form.get("startDate"))
    startTime = parse_time(request.form.get("startTime"))
    endDate: date = parse_date(request.form.get("endDate"))
    endTime = parse_time(request.form.get("endTime"))

    assessment: Exam | None = get_exam(int(id))
    if assessment:
        assessment.start_date = startDate
        assessment.start_time = startTime
        assessment.end_time = endTime
        db.session.commit()

        clash: bool = ClashContext().detect_clash(assessment)
        if clash:
            session["message"] = (
                assessment.course_code
                + " - Clash detected! The maximum amount of exams for this level has been exceeded."
            )
        else:
            session["message"] = "Assessment modified"
    return session["message"]


# Sends confirmation email to staff upon registering
@staff_views.route("/send_email", methods=["GET", "POST"])
def send_email():
    mail = Mail(app)  # Create mail instance

    subject = "Test Email!"
    receiver = request.form.get("email")
    body = "Successful Registration"

    msg = Message(subject, recipients=[receiver], html=body)
    mail.send(msg)
    return render_template("login.html")


# Gets account page
@staff_views.route("/account", methods=["GET"])
@jwt_required()
def get_account_page():
    staff: Staff | None = get_staff(get_jwt_identity())
    if staff is None:
        return render_template("login.html")
    courses: list[Course] = get_all_courses()
    registered_courses: list[Course] = get_registered_courses(staff.id)
    registered_course_codes: list[str] = [
        course.course_code for course in registered_courses
    ]
    return render_template(
        "account.html", courses=courses, registered_courses=registered_course_codes
    )


# Assign course to staff
@staff_views.route("/account", methods=["POST"])
@jwt_required()
def get_selected_courses():
    staff: Staff | None = get_staff(get_jwt_identity())
    if staff is None:
        return redirect(url_for("staff_views.get_account_page"))
    course_codes_json: str | None = request.form.get("courseCodes")
    if course_codes_json:
        course_codes = json.loads(course_codes_json)
        for course_code in course_codes:
            add_instructor(staff.id, course_code)

        return redirect(url_for("staff_views.get_account_page"))


# Gets exams page
@staff_views.route("/assessments", methods=["GET"])
@jwt_required()
def get_exams_page():
    staff: Staff | None = get_staff(get_jwt_identity())
    if staff is None:
        return render_template("login.html")
    registered_courses: list[Course] = get_registered_courses(staff.id)
    exams: list[dict] = [
        assessment.to_json()
        for course in registered_courses
        for assessment in get_exams_by_course(course.course_code)
    ]
    registered_course_codes: list[str] = [
        course.course_code for course in registered_courses
    ]
    return render_template(
        "assessments.html", courses=registered_course_codes, exams=exams
    )

# Get settings page
@staff_views.route("/settings", methods=["GET"])
@jwt_required()
def get_settings_page():
    return render_template("settings.html")


# Route to change password of user
@staff_views.route("/settings", methods=["POST"])
@jwt_required()
def changePassword():
    newPassword: str | None = request.form["password"]
    staff: Staff | None = get_staff(get_jwt_identity())
    staff.set_password(newPassword)
    db.session.commit()
    return render_template("settings.html")
