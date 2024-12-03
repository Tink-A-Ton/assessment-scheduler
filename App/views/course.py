from flask import Blueprint, request, render_template, redirect, url_for, flash
from werkzeug import Response
from ..models import Semester
from ..controllers import create_course, delete_course, edit_course
from ..controllers import get_courses, get_course, get_semester, role_required

course_views = Blueprint("course_views", __name__, template_folder="../templates")


@course_views.route("/modifyCourse/<string:course_code>", methods=["GET"])
@role_required("Admin")
def get_update_course_page(course_code) -> str:
    return render_template("updateCourse.html", course=get_course(course_code))


@course_views.route("/get_courses", methods=["GET"])
@role_required("Admin")
def get_courses_page() -> str:
    return render_template("courses.html", courses=get_courses())


@course_views.route("/newCourse", methods=["GET"])
@role_required("Admin")
def get_add_course_page() -> str:
    return render_template("addCourse.html")


@course_views.route("/updateCourse", methods=["GET"])
@role_required("Admin")
def update_course_page() -> str:
    return render_template("updateCourse.html")


@course_views.route("/updateCourse", methods=["POST"])
@role_required("Admin")
def update_course() -> Response:
    data: dict[str, str] = request.form
    edit_course(data["code"], data["title"], int(data["level"]))
    flash("Course Updated Successfully!")
    return redirect(url_for("course_views.get_courses_page"))


@course_views.route("/addNewCourse", methods=["POST"])
@role_required("Admin")
def add_course_action() -> Response:
    data: dict[str, str] = request.form
    sem: Semester = get_semester()
    create_course(data["course_code"], data["title"], int(data["level"]), sem.id)
    return redirect(url_for("course_views.get_courses_page"))


@course_views.route("/deleteCourse/<string:course_code>", methods=["POST"])
@role_required("Admin")
def delete_course_action(course_code) -> Response:
    delete_course(course_code)
    flash("Course Deleted Successfully!")
    return redirect(url_for("course_views.get_courses_page"))
