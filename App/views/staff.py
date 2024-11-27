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
from flask_login import current_user
from flask import current_app as app
from flask_mail import Mail, Message
from sqlalchemy import not_
from werkzeug import Response
from App.database import db
import json
from flask_jwt_extended import current_user as jwt_current_user, get_jwt_identity
from flask_jwt_extended import jwt_required
from datetime import date, time, timedelta
import time
from App.models.course import Course
from App.models.courseAssessment import CourseAssessment
from App.models.staff import Staff
from App.models.semester import Semester
from App.controllers.staff import (
    get_registered_courses,
    create_staff,
    add_course_instructor,
)
from App.controllers.course import get_all_courses, get_courses_by_level
from App.controllers.user import get_user, get_user_by_email
from App.controllers.assessment import (
    get_assessments_by_course,
    get_assessment_by_id,
    get_assessments_by_level,
    get_course,
    add_assessment,
    delete_assessment_by_id,
    get_assessments,
)
from App.controllers.initialize import parse_date, parse_time
from App.models.user import User

staff_views = Blueprint("staff_views", __name__, template_folder="../templates")


# Gets Signup Page
@staff_views.route("/signup", methods=["GET"])
def get_signup_page():
    return render_template("signup.html")


# Gets Calendar Page
@staff_views.route("/calendar", methods=["GET"])
@jwt_required()
def get_calendar_page():
    user: User | None = get_user_by_email(
        get_jwt_identity()
    )  # gets u_id from email token

    all_courses: list[Course] = get_all_courses()
    registered_courses: list[Course] = get_registered_courses(user.id)
    other_courses: list[Course] = [
        course for course in all_courses if course not in registered_courses
    ]
    staff_courses: list[dict] = [course.to_json() for course in registered_courses]
    staff_assessments: list[dict] = [
        format_assessment(assessment)
        for course in registered_courses
        for assessment in get_assessments_by_course(course.course_code)
    ]

    other_assessments: list[dict] = [
        format_assessment(assessment)
        for assessment in get_assessments()
        if not assessment.clash_detected
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
        staff_assessments=staff_assessments,
        semester=semester_details,
        other_assessments=other_assessments,
        messages=messages,
    )


@staff_views.route("/calendar", methods=["POST"])
@jwt_required()
def update_calendar_page():
    id: str | None = request.form.get("id")
    startDate: date = parse_date(request.form.get("startDate"))
    startTime: time = parse_time(request.form.get("startTime"))
    endDate: date = parse_date(request.form.get("endDate"))
    endTime: time = parse_time(request.form.get("endTime"))

    assessment: CourseAssessment | None = get_assessment_by_id(id)
    if assessment:
        assessment.start_date = startDate
        assessment.end_date = endDate
        assessment.start_time = startTime
        assessment.end_time = endTime
        db.session.commit()
        clash = detect_clash(assessment.id)
        if clash:
            assessment.clash_detected = True
            db.session.commit()
            session["message"] = (
                assessment.courseCode
                + " - Clash detected! The maximum amount of assessments for this level has been exceeded."
            )
        else:
            session["message"] = "Assessment modified"
    return session["message"]


def detect_clash(id) -> bool:
    #     clash = 0
    #     sem = Semester.query.order_by(
    #         Semester.id.desc()
    #     ).first()  # get the weekly max num of assessments allowed per level
    #     max = sem.maxAssessments
    #     new_assessment = get_assessment_by_id(id)  # get current assessment info
    #     compare_code = new_assessment.courseCode.replace(" ", "")
    #     all_assessments = AssessmentType.query.filter(
    #         not_(AssessmentType.a_ID.in_([2, 4, 8]))
    #     ).all()
    #     if not new_assessment.endDate:  # dates not set yet
    #         return False
    #     relevant_assessments = []
    #     for a in all_assessments:
    #         code = a.courseCode.replace(" ", "")
    #         if (code[4] == compare_code[4]) and (
    #             a.id != new_assessment.id
    #         ):  # course are in the same level
    #             if a.startDate is not None:  # assessment has been scheduled
    #                 relevant_assessments.append(a)

    #     sunday, saturday = get_week_range(new_assessment.endDate.isoformat())
    #     for a in relevant_assessments:
    #         dueDate = a.endDate
    #         if sunday <= dueDate <= saturday:
    #             clash = clash + 1

    #     return clash >= max

    # def get_week_range(iso_date_str):
    #     date_obj = date.fromisoformat(iso_date_str)
    #     day_of_week = date_obj.weekday()

    #     if day_of_week != 6:
    #         days_to_subtract = (day_of_week + 1) % 7
    #     else:
    #         days_to_subtract = 0

    #     sunday_date = date_obj - timedelta(days=days_to_subtract)  # get sunday's date
    #     saturday_date = sunday_date + timedelta(days=6)  # get saturday's date
    #     return sunday_date, saturday_date
    return False


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


# Retrieves staff info and stores it in database ie. register new staff
@staff_views.route("/register", methods=["POST"])
def register_staff_action():
    firstname: str | None = request.form.get("firstName")
    lastname: str | None = request.form.get("lastName")
    staff_id: str | None = request.form.get("staffID")
    position: str | None = request.form.get("status")
    email: str | None = request.form.get("email")
    password: str | None = request.form.get("password")

    create_staff(
        first_name=firstname,
        last_name=lastname,
        id=staff_id,
        position=position,
        email=email,
        password=password,
    )
    return render_template("login.html")
    # return redirect(url_for('staff_views.send_email'))


# Gets account page
@staff_views.route("/account", methods=["GET"])
@jwt_required()
def get_account_page():
    user: User = get_user_by_email(get_jwt_identity())
    courses: list[Course] = get_all_courses()
    registered_courses: list[Course] = get_registered_courses(user.id)
    registered_course_codes: list[Course] = [
        course.course_code for course in registered_courses
    ]
    print(registered_courses)
    return render_template(
        "account.html", courses=courses, registered_courses=registered_course_codes
    )


# Assign course to staff
@staff_views.route("/account", methods=["POST"])
@jwt_required()
def get_selected_courses():
    staff: User | None = get_user_by_email(get_jwt_identity())
    print(get_jwt_identity())
    course_codes_json = request.form.get("courseCodes")
    course_codes = json.loads(course_codes_json)
    for course_code in course_codes:
        add_course_instructor(staff.id, course_code)

    return redirect(url_for("staff_views.get_account_page"))


# Gets assessments page
@staff_views.route("/assessments", methods=["GET"])
@jwt_required()
def get_assessments_page():
    user: User | None = get_user_by_email(get_jwt_identity())
    registered_courses: list[Course] = get_registered_courses(user.id)
    assessments: list[dict] = [
        format_assessment(assessment)
        for course in registered_courses
        for assessment in get_assessments_by_course(course.course_code)
    ]
    registered_course_codes: list[Course] = [
        course.course_code for course in registered_courses
    ]
    print(assessments)
    return render_template(
        "assessments.html", courses=registered_course_codes, assessments=assessments
    )


# Gets add assessment page
@staff_views.route("/addAssessment", methods=["GET"])
@jwt_required()
def get_add_assessments_page():
    user: User | None = get_user_by_email(get_jwt_identity())
    registered_courses: list[Course] = get_registered_courses(user.id)
    registered_course_codes: list[Course] = [
        course.course_code for course in registered_courses
    ]
    return render_template(
        "addAssessment.html",
        courses=registered_course_codes,
    )


# Retrieves assessment info and creates new assessment for course
@staff_views.route("/addAssessment", methods=["POST"])
@jwt_required()
def add_assessments_action():
    course: str | None = request.form.get("myCourses")
    type: str | None = request.form.get("AssessmentType")
    startDate: date = parse_date(request.form.get("startDate"))
    endDate: date = parse_date(request.form.get("endDate"))
    startTime: time = parse_time(request.form.get("startTime"))
    endTime: time = parse_time(request.form.get("endTime"))

    if startDate == "" or endDate == "" or startTime == "" or endTime == "":
        startDate = None
        endDate = None
        startTime = None
        endTime = None
    print(course)
    if add_assessment(
        course_code=course,
        category=type,
        start_date=startDate,
        end_date=endDate,
        start_time=startTime,
        end_time=endTime,
        clash_detected=False,
    ):
        flash("AssessmentType created !")
    # if newAsm.startDate:
    #     clash = detect_clash(newAsm.id)
    #     if clash:
    #         newAsm.clashDetected = True
    #         db.session.commit()
    #         flash(
    #             "Clash detected! The maximum amount of assessments for this level has been exceeded."
    #         )
    #         time.sleep(1)

    return redirect(url_for("staff_views.get_assessments_page"))


# Modify selected assessment
@staff_views.route("/modifyAssessment/<string:id>", methods=["GET"])
def get_modify_assessments_page(id):
    assessment: CourseAssessment | None = get_assessment_by_id(id)
    return render_template("modifyAssessment.html", ca=assessment)


# Gets Update assessment Page
@staff_views.route("/modifyAssessment/<string:id>", methods=["POST"])
def modify_assessment(id):
    course: str | None = request.form.get("myCourses")
    type: str | None = request.form.get("AssessmentType")
    start_date: date = parse_date(request.form.get("startDate"))
    end_date: date = parse_date(request.form.get("endDate"))
    start_time: time = parse_time(request.form.get("startTime"))
    end_time: time = parse_time(request.form.get("endTime"))

    assessment: CourseAssessment | None = get_assessment_by_id(id)
    if assessment:
        if start_date != "" and end_date != "" and start_time != "" and end_time != "":
            assessment.start_date = start_date
            assessment.end_date = end_date
            assessment.start_time = start_time
            assessment.end_time = end_time
        db.session.commit()
        clash = detect_clash(assessment.id)
        if clash:
            assessment.clash_detected = True
            db.session.commit()
            flash(
                "Clash detected! The maximum amount of assessments for this level has been exceeded."
            )
            time.sleep(1)
    return redirect(url_for("staff_views.get_assessments_page"))


# Delete selected assessment
@staff_views.route("/deleteAssessment/<int:assessment_id>", methods=["GET"])
def delete_assessment(assessment_id) -> Response:
    if delete_assessment_by_id(assessment_id=assessment_id):
        print("Assessment ", assessment_id, " deleted")
    else:
        flash("Unable to delete Assessment ", assessment_id)
    return redirect(url_for("staff_views.get_assessments_page"))


# Get settings page
@staff_views.route("/settings", methods=["GET"])
@jwt_required()
def get_settings_page():
    return render_template("settings.html")


# Route to change password of user
@staff_views.route("/settings", methods=["POST"])
@jwt_required()
def changePassword():
    newPassword: str | None = request.form.get("password")
    user: User = get_user_by_email(get_jwt_identity())
    if user and newPassword:
        user.set_password(newPassword)
        db.session.commit()
    return render_template("settings.html")


def format_assessment(assessment: CourseAssessment) -> dict:
    assessment_json: dict = assessment.to_json()
    return assessment_json
