from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_jwt_extended import jwt_required
from werkzeug import Response
from ..models import Admin, Exam
from ..controllers import create_course, delete_course, edit_course, process_file
from ..controllers import get_all_courses, get_course, get_search_results, get_clashes
from ..controllers import deny_override, allow_override, add_semester


admin_views = Blueprint("admin_views", __name__, template_folder="../templates")


@admin_views.route("/semester", methods=["GET"])
@jwt_required(Admin)
def get_upload_page() -> str:
    return render_template("semester.html")


@admin_views.route("/uploadFiles", methods=["GET"])
@jwt_required(Admin)
def get_uploadFiles_page() -> str:
    return render_template("uploadFiles.html")


@admin_views.route("/modifyCourse/<string:course_code>", methods=["GET"])
@jwt_required(Admin)
def get_update_course(course_code) -> str:
    return render_template("updateCourse.html", course=get_course(course_code))


@admin_views.route("/coursesList", methods=["GET"])
@jwt_required(Admin)
def index() -> str:
    return render_template("courses.html")


@admin_views.route("/get_courses", methods=["GET"])
@jwt_required(Admin)
def get_courses() -> str:
    return render_template("courses.html", courses=get_all_courses())


@admin_views.route("/newCourse", methods=["GET"])
@jwt_required(Admin)
def get_new_course() -> str:
    return render_template("addCourse.html")


@admin_views.route("/newSemester", methods=["POST"])
@jwt_required(Admin)
def new_semester_action() -> str:
    add_semester(
        request.form["teachingBegins"],
        request.form["teachingEnds"],
        int(request.form["semester"]),
        int(request.form["maxAssessments"]),
    )
    return render_template("uploadFiles.html")


@admin_views.route("/uploadcourse", methods=["POST"])
@jwt_required(Admin)
def upload_course_file() -> str | Response:
    file = request.files["file"]
    if file.filename == "":
        return render_template("uploadFiles.html", message="No file selected!")
    process_file(file)
    return redirect(url_for("admin_views.get_courses"))


@admin_views.route("/updateCourse", methods=["GET"])
@jwt_required(Admin)
def update_course_page() -> str:
    return render_template("updateCourse.html")


@admin_views.route("/clashes", methods=["GET"])
@jwt_required(Admin)
def get_clashes_page() -> str:
    search_results: list[Exam] = get_search_results(request.args["start_date"])
    return render_template("clashes.html", exams=get_clashes(), results=search_results)


@admin_views.route("/updateCourse", methods=["POST"])
@jwt_required(Admin)
def update_course() -> Response:
    data: dict[str, str] = request.form
    # programme = request.form.get('programme')
    edit_course(data["code"], int(data["semester"]), data["title"], int(data["level"]))
    flash("Course Updated Successfully!")
    return redirect(url_for("admin_views.get_courses"))


@admin_views.route("/addNewCourse", methods=["POST"])
@jwt_required(Admin)
def add_course_action() -> Response:
    data: dict[str, str] = request.form
    create_course(
        data["course_code"], data["title"], int(data["level"]), int(data["semester"])
    )
    return redirect(url_for("admin_views.get_courses"))


@admin_views.route("/deleteCourse/<string:course_code>", methods=["POST"])
@jwt_required(Admin)
def delete_course_action(course_code) -> Response:
    delete_course(course_code)
    flash("Course Deleted Successfully!")
    return redirect(url_for("admin_views.get_courses"))


@admin_views.route("/acceptOverride/<int:assessment_id>", methods=["POST"])
@jwt_required(Admin)
def accept_override(id: int) -> Response:
    allow_override(id)
    return redirect(url_for("admin_views.get_clashes_page"))


@admin_views.route("/rejectOverride/<int:assessment_id>", methods=["POST"])
@jwt_required(Admin)
def reject_override(id: int) -> Response:
    deny_override(id)
    return redirect(url_for("admin_views.get_clashes_page"))
