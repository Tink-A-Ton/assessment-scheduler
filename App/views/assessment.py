from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    flash,
)
from werkzeug import Response
from App.database import db
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from datetime import date, time
import time
from ..models import Course, Exam, Staff
from App.controllers.staff import (
    get_registered_courses,
    get_staff,
)
from App.controllers.exam import (
    get_exam,
    get_exams_by_course,
    create_exam,
    delete_exam,
)
from App.controllers.initialize import parse_date, parse_time
from App.models import Staff, ClashContext

assessment_views = Blueprint("assessment_views", __name__, template_folder="../templates")


@assessment_views.route("/modifyAssessment/<string:id>", methods=["GET"])
@jwt_required(Staff)
def get_modify_exams_page(id) -> str:
    assessment: Exam | None = get_exam(id)
    return render_template("modifyAssessment.html", course_assessment=assessment)


@assessment_views.route("/assessments", methods=["GET"])
@jwt_required(Staff)
def get_exams_page() -> str:
    staff: Staff | None = get_staff(get_jwt_identity())
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


@assessment_views.route("/addAssessment", methods=["GET"])
@jwt_required(Staff)
def get_add_exams_page() -> str:
    staff: Staff | None = get_staff(get_jwt_identity())
    registered_courses: list[Course] = get_registered_courses(staff.id)
    registered_course_codes: list[str] = [
        course.course_code for course in registered_courses
    ]
    return render_template(
        "addAssessment.html",
        courses=registered_course_codes,
    )


@assessment_views.route("/addAssessment", methods=["POST"])
@jwt_required(Staff)
def add_exams_action():
    course: str | None = request.form.get("myCourses")
    type: str | None = request.form.get("AssessmentType")
    startDate: date = parse_date(request.form.get("startDate"))
    endDate: date = parse_date(request.form.get("endDate"))
    startTime = parse_time(request.form.get("startTime"))
    endTime = parse_time(request.form.get("endTime"))
    startTime = parse_time(request.form.get("startTime"))
    endTime = parse_time(request.form.get("endTime"))
    rule1 = request.form.get("rule1")
    rule2 = request.form.get("rule2")

    if course is None:
        return

    assessment: Exam = create_exam(course, startDate, startTime, endTime, False)
    flash("AssessmentType created !")
    if not startDate:
        return redirect(url_for("assessment_views.get_exams_page"))

    context = ClashContext()
    if rule1:
        context.add_rule("rule1")
    if rule2:
        context.add_rule("rule2")

    clash: bool = context.detect_clash(assessment)
    if clash:
        flash(
            "Clash detected! The maximum amount of exams for this level has been exceeded."
        )
        time.sleep(1)
    return redirect(url_for("assessment_views.get_exams_page"))


@assessment_views.route("/modifyAssessment/<string:id>", methods=["POST"])
@jwt_required(Staff)
def modify_assessment(id):
    start_date: date = parse_date(request.form.get("startDate"))
    end_date: date = parse_date(request.form.get("endDate"))
    start_time = parse_time(request.form.get("startTime"))
    end_time = parse_time(request.form.get("endTime"))
    rule1 = request.form.get("rule1")
    rule2 = request.form.get("rule2")
    assessment: Exam | None = get_exam(id)

    if assessment:
        assessment.start_date = start_date
        assessment.start_time = start_time
        assessment.end_time = end_time
        db.session.commit()
        context = ClashContext()
        if rule1:
            context.add_rule("rule1")
        if rule2:
            context.add_rule("rule2")
        clash: bool = context.detect_clash(assessment)
        print(clash)
        if clash:
            flash(
                "Clash detected! The maximum amount of exams for this level has been exceeded."
            )
    return redirect(url_for("assessment_views.get_exams_page"))


# Delete selected assessment
@assessment_views.route("/deleteAssessment/<int:assessment_id>", methods=["GET"])
@jwt_required(Staff)
def delete_assessment(assessment_id) -> Response:
    if delete_exam(assessment_id):
        print("Assessment ", assessment_id, " deleted")
    else:
        flash("Unable to delete Assessment ", assessment_id)
    return redirect(url_for("assessment_views.get_exams_page"))
