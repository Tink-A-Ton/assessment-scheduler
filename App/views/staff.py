from flask import Blueprint, request, render_template, redirect, url_for, session
from werkzeug import Response
import json
from ..models import Course, Exam
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..controllers import get_registered_courses, get_staff_courses
from ..controllers import get_semester_json, get_courses, get_available_courses
from ..controllers import detect_exam_clash, update_password, add_instructor
from ..controllers import get_exams_json, get_staff_exams, update_exam

staff_views = Blueprint("staff_views", __name__, template_folder="../templates")


@staff_views.route("/account", methods=["GET"])
@jwt_required()
def get_account_page() -> str:
    courses: list[Course] = get_courses()
    registered_courses: list[Course] = get_registered_courses(get_jwt_identity())
    course_codes: list[str] = [c.course_code for c in registered_courses]
    return render_template(
        "account.html", courses=courses, registered_courses=course_codes
    )


@staff_views.route("/calendar", methods=["GET"])
@jwt_required()
def get_calendar_page() -> str:
    id: int = get_jwt_identity()
    registered_courses: list[Course] = get_registered_courses(id)
    messages: list[str] = [session.pop("message")] if "message" in session else []

    return render_template(
        "index.html",
        courses=get_available_courses(registered_courses),
        staff_courses=get_staff_courses(id),
        staff_exams=get_staff_exams(id),
        semester=get_semester_json(),
        other_exams=get_exams_json(),
        messages=messages,
    )


@staff_views.route("/calendar", methods=["POST"])
@jwt_required()
def update_calendar_page() -> str:
    data: dict[str, str] = request.form
    exam: Exam | None = update_exam(
        int(data["id"]), data["startDate"], data["startTime"], data["endTime"]
    )
    if detect_exam_clash(exam):
        session["message"] = "Clash detected, maximum exams for this level  exceeded."
    else:
        session["message"] = "Assessment modified"
    return session["message"]


@staff_views.route("/account", methods=["POST"])
@jwt_required()
def get_selected_courses() -> Response | None:
    course_codes: list[str] = json.loads(request.form.get("courseCodes", "[]"))
    for course_code in course_codes:
        add_instructor(get_jwt_identity(), course_code)
    return redirect(url_for("staff_views.get_account_page"))


@staff_views.route("/settings", methods=["POST"])
@jwt_required()
def changePassword() -> str:
    update_password(get_jwt_identity(), request.form["password"])
    return render_template("settings.html")
