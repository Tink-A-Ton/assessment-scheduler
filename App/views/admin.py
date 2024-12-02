from flask import Blueprint, request, render_template, redirect, url_for
from flask_jwt_extended import jwt_required
from werkzeug import Response
from ..models import Admin, Exam
from ..controllers import process_file, get_search_results, get_clashes
from ..controllers import deny_override, allow_override, create_semester


admin_views = Blueprint("admin_views", __name__, template_folder="../templates")


@admin_views.route("/semester", methods=["GET"])
@jwt_required(Admin)
def get_upload_page() -> str:
    return render_template("semester.html")


@admin_views.route("/uploadFiles", methods=["GET"])
@jwt_required(Admin)
def get_uploadFiles_page() -> str:
    return render_template("uploadFiles.html")


@admin_views.route("/newSemester", methods=["POST"])
@jwt_required(Admin)
def new_semester_action() -> str:
    create_semester(
        request.form["teachingBegins"],
        request.form["teachingEnds"],
        int(request.form["semester"]),
        int(request.form["maxAssessments"]),
    )
    return render_template("uploadFiles.html")


@admin_views.route("/clashes", methods=["GET"])
@jwt_required(Admin)
def get_clashes_page() -> str:
    search_results: list[Exam] = get_search_results(request.args.get("start_date"))
    return render_template("clashes.html", exams=get_clashes(), results=search_results)


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


@admin_views.route("/uploadcourse", methods=["POST"])
@jwt_required(Admin)
def upload_course_file() -> str | Response:
    file = request.files["file"]
    if file.filename == "":
        return render_template("uploadFiles.html", message="No file selected!")
    process_file(file)
    return redirect(url_for("course_views.get_courses_page"))
