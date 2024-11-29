from flask import Blueprint, request, render_template, redirect, url_for, flash
from werkzeug import Response
from App.database import db
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from datetime import date, time
import time as sleep_timer
from ..models import Course, Exam, Staff
from ..controllers import (
    get_exam,
    get_exams_by_course,
    create_exam,
    delete_exam,
    update_exam,
    get_registered_courses,
    get_staff_courses,
    get_staff,
)
from App.controllers.clash import detect_exam_clash
from App.controllers.initialize import parse_date, parse_time
from App.models import Staff

exam_views = Blueprint("exam_views", __name__, template_folder="../templates")


def get_current_staff() -> Staff:
    return get_staff(get_jwt_identity())


@exam_views.route("/assessments", methods=["GET"])
@jwt_required(Staff)
def get_exams_page() -> str:
    staff: Staff | None = get_current_staff()
    staff_courses: list[dict] = get_staff_courses(staff.id)
    exams: list[dict] = [
        exam.to_json()
        for course in staff_courses
        for exam in get_exams_by_course(course["course_code"])
    ]
    return render_template("assessments.html", courses=staff_courses, exams=exams)


@exam_views.route("/modifyAssessment/<int:id>", methods=["GET"])
@jwt_required(Staff)
def get_modify_exam_page(id) -> str:
    exam: Exam | None = get_exam(id)
    return render_template("modifyAssessment.html", course_assessment=exam)


@exam_views.route("/addAssessment", methods=["GET"])
@jwt_required(Staff)
def get_add_exams_page() -> str:
    staff: Staff | None = get_current_staff()
    registered_courses: list[Course] = get_registered_courses(staff.id)
    return render_template(
        "addAssessment.html",
        courses=registered_courses,
    )


@exam_views.route("/addAssessment", methods=["POST"])
@jwt_required(Staff)
def add_exam_action() -> Response | str:
    data: dict[str, str] = request.form
    exam: Exam = create_exam(
        data["course"],
        parse_date(data["startDate"]),
        parse_time(data["startTime"]),
        parse_time(data["endTime"]),
        False,
    )
    clash: bool = detect_exam_clash(
        exam, request.form.get("rule1"), request.form.get("rule2")
    )
    if clash:
        flash("Clash Detected! Reschedule exam or send to ADMIN for approval")
        sleep_timer.sleep(1)
    return redirect(url_for("exam_views.get_exams_page"))


@exam_views.route("/modifyAssessment/<int:id>", methods=["POST"])
@jwt_required(Staff)
def modify_exam_action(id) -> Response:
    data: dict[str, str] = request.form
    exam: None | Exam = update_exam(
        id, data["startDate"], data["startTime"], data["endTime"]
    )
    if exam:
        flash(f"Exam Details Updated !")
        clash: bool = detect_exam_clash(
            exam, request.form.get("rule1"), request.form.get("rule2")
        )
        if clash:
            flash("Clash Detected! Reschedule exam or send to ADMIN for approval")
    return redirect(url_for("exam_views.get_exams_page"))


@exam_views.route("/deleteAssessment/<int:exam_id>", methods=["GET"])
@jwt_required(Staff)
def delete_exam_action(exam_id) -> Response:
    if delete_exam(exam_id):
        flash("Exam deleted")
    else:
        flash("Unable to delete exam ", exam_id)
    return redirect(url_for("exam_views.get_exams_page"))
