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
from App.database import db
import json
from flask_jwt_extended import current_user as jwt_current_user, get_jwt_identity
from flask_jwt_extended import jwt_required
from datetime import date, timedelta
import time
from App.models.assessment import Assessment
from App.models.course import Course
from App.models.courseAssessment import CourseAssessment
from App.models.staff import Staff
from App.models.semester import Semester
from App.controllers.staff import (
    get_registered_courses, create_staff,
    add_course_instructor
)
from App.controllers.course import get_all_courses, get_courses_by_level
from App.controllers.user import get_user, get_user_by_email
from App.controllers.assessment import (
    get_assessments_by_course, get_assessment_types, 
    get_assessment_by_id, get_assessment_types, 
    get_assessments_by_level, get_course,
    add_assessment
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
    id = get_user(get_jwt_identity())  # gets u_id from email token

    # Get courses for filter
    courses: list[Course] = []
    all_courses: list[Course] = get_all_courses()
    staff_courses: list[Course] = get_registered_courses(id)
    for course in all_courses:
        if course not in staff_courses:
            courses.append(course)

    # Get assessments for registered courses
    all_assessments = []
    for course in staff_courses:
        all_assessments = all_assessments + get_assessments_by_course(course.course_code)

    # Format assessments for calendar js - registered courses
    staff_assessments = []
    for assessment in all_assessments:
        assessment_json = assessment.to_json()
        staff_assessments.append(assessment_json)

    # Get assessments for all other courses (for filters)
    other_assessments: list[CourseAssessment] = []
    for course in courses:
        other_assessments = other_assessments + get_assessments_by_course(course.course_code)

    # Format assessments for calendar js - filters
    assessments = []
    for assessment in other_assessments:
        if not assessment.clash_detected:
            assessment_json: dict = assessment.to_json()
            assessments.append(assessment_json)
    # Ensure courses, staff_courses, and assessments are not empty
    if not courses:
        courses = []
    if not staff_courses:
        staff_courses = []
    if not staff_assessments:
        staff_assessments = []
    if not assessments:
        assessments = []

    sem: Semester = Semester.query.order_by(Semester.id.desc()).first()
    semester = {"start": sem.start_date, "end": sem.end_date}

    messages = []
    message = session.pop("message", None)
    if message:
        messages.append(message)
    return render_template(
        "index.html",
        courses=courses,
        staff_courses=staff_courses,
        staff_assessments=staff_assessments,
        semester=semester,
        other_assessments=assessments,
        messages=messages,
    )


@staff_views.route("/calendar", methods=["POST"])
@jwt_required()
def update_calendar_page():
    # Retrieve data from page
    id = request.form.get("id")
    startDate = request.form.get("startDate")
    startTime = request.form.get("startTime")
    endDate = request.form.get("endDate")
    endTime = request.form.get("endTime")

    # Get course assessment
    assessment = get_assessment_by_id(id)
    if assessment:
        assessment.startDate = startDate
        assessment.endDate = endDate
        assessment.startTime = startTime
        assessment.endTime = endTime

        db.session.commit()

        clash = detect_clash(assessment.id)
        if clash:
            assessment.clashDetected = True
            db.session.commit()
            session["message"] = (
                assessment.courseCode
                + " - Clash detected! The maximum amount of assessments for this level has been exceeded."
            )
        else:
            session["message"] = "Assessment modified"
    return session["message"]


def detect_clash(id):
#     clash = 0
#     sem = Semester.query.order_by(
#         Semester.id.desc()
#     ).first()  # get the weekly max num of assessments allowed per level
#     max = sem.maxAssessments
#     new_assessment = get_assessment_by_id(id)  # get current assessment info
#     compare_code = new_assessment.courseCode.replace(" ", "")
#     all_assessments = Assessment.query.filter(
#         not_(Assessment.a_ID.in_([2, 4, 8]))
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
    firstname = request.form.get("firstName")
    lastname = request.form.get("lastName")
    staff_id = request.form.get("staffID")
    position = request.form.get("status")
    email = request.form.get("email")
    password = request.form.get("password")

    create_staff(first_name=firstname, last_name=lastname, id=staff_id, position=position, email=email, password=password)
    return render_template("login.html")
    # return redirect(url_for('staff_views.send_email'))


# Gets account page
@staff_views.route("/account", methods=["GET"])
@jwt_required()
def get_account_page():
    user: User = get_user_by_email(get_jwt_identity())
    courses: list[Course] = get_all_courses()
    registered_courses: list[Course] = get_registered_courses(user.id)
    registered_course_codes: list[Course] = [course.course_code for course in registered_courses]
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
    assessments = []
    for course in registered_courses:
        for assessment in get_assessments_by_course(course.course_code):
            assessment_json = assessment.to_json()
            assessments.append(assessment_json)
    registered_course_codes: list[Course] = [course.course_code for course in registered_courses]
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
    registered_course_codes: list[Course] = [course.course_code for course in registered_courses]
    assessment_types: list[Assessment] = get_assessment_types()
    print("ASSESSMENT TYPES: ", assessment_types)
    return render_template(
        "addAssessment.html", courses=registered_course_codes, assessment_types=assessment_types
    )


# Retrieves assessment info and creates new assessment for course
@staff_views.route("/addAssessment", methods=["POST"])
@jwt_required()
def add_assessments_action():
    course: str | None = request.form.get("myCourses")
    asmType: str | None = request.form.get("AssessmentType")
    startDate: date = parse_date(request.form.get("startDate"))
    endDate: date = parse_date(request.form.get("endDate"))
    startTime = parse_time(request.form.get("startTime"))
    endTime = parse_time(request.form.get("endTime"))

    if startDate == "" or endDate == "" or startTime == "" or endTime == "":
        startDate = None
        endDate = None
        startTime = None
        endTime = None
    print(course)
    if add_assessment(
        course_code=course, category=asmType, 
        start_date=startDate, end_date=endDate, 
        start_time=startTime, end_time=endTime,
        clash_detected=False
    ):
        flash("Assessment created !")
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
    allAsm: list[Assessment] = get_assessment_types()  # get assessment types
    assessment: CourseAssessment | None = get_assessment_by_id(id)  # get assessment details
    return render_template("modifyAssessment.html", assessments=allAsm, ca=assessment)


# Gets Update assessment Page
@staff_views.route("/modifyAssessment/<string:id>", methods=["POST"])
def modify_assessment(id):
    if request.method == "POST":
        # get form details
        course = request.form.get("staff_courses")
        asmType = request.form.get("AssessmentType")
        startDate = request.form.get("startDate")
        endDate = request.form.get("endDate")
        startTime = request.form.get("startTime")
        endTime = request.form.get("endTime")

        # update record
        assessment = get_assessment_by_id(id)
        if assessment:
            assessment.a_ID = asmType
            if startDate != "" and endDate != "" and startTime != "" and endTime != "":
                assessment.startDate = startDate
                assessment.endDate = endDate
                assessment.startTime = startTime
                assessment.endTime = endTime

            db.session.commit()

            clash = detect_clash(assessment.id)
            if clash:
                assessment.clashDetected = True
                db.session.commit()
                flash(
                    "Clash detected! The maximum amount of assessments for this level has been exceeded."
                )
                time.sleep(1)

    return redirect(url_for("staff_views.get_assessments_page"))


# Delete selected assessment
@staff_views.route("/deleteAssessment/<string:caNum>", methods=["GET"])
def delete_assessment(caNum):
    courseAsm = get_assessment_by_id(caNum)  # Gets selected assessment for course
    delete_assessment(courseAsm)
    print(caNum, " deleted")
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

    if request.method == "POST":
        # get new password
        newPassword = request.form.get("password")
        # print(newPassword)

        # get email of current user
        current_user_email = get_jwt_identity()
        # print(current_user_email)

        # find user by email
        user = Staff.query.filter_by(email=current_user_email).first()
        # print(user)

        if user:
            # update the password
            user.set_password(newPassword)

            # commit changes to DB
            db.session.commit()

    return render_template("settings.html")
