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
    edit_exam,
    get_registered_courses,
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
    registered_courses: list[Course] = get_registered_courses(staff.id)
    exams: list[dict] = [
        exam.to_json()
        for course in registered_courses
        for exam in get_exams_by_course(course.course_code)
    ]
    staff_courses: list[dict] = [course.to_json() for course in registered_courses]
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
    registered_course_codes: list[str] = [
        course.course_code for course in registered_courses
    ]
    return render_template(
        "addAssessment.html",
        courses=registered_course_codes,
    )


@exam_views.route("/addAssessment", methods=["POST"])
@jwt_required(Staff)
def add_exam_action() -> Response | str:
    course_code: str | None = request.form.get("course")
    start_date: date = parse_date(request.form.get("startDate"))
    start_time: time = parse_time(request.form.get("startTime"))
    end_time: time = parse_time(request.form.get("endTime"))
    if course_code is None:
        flash("Course is required to schedule an exam")
        return get_exams_page()
    exam: Exam = create_exam(course_code, start_date, start_time, end_time, False)
    flash(f"Exam for {course_code} created !")
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
    start_date: date = parse_date(request.form.get("startDate"))
    start_time: time = parse_time(request.form.get("startTime"))
    end_time: time = parse_time(request.form.get("endTime"))
    exam: None | Exam = edit_exam(id, start_date, start_time, end_time)
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
