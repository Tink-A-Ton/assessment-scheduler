from flask import Blueprint, request, render_template, redirect, url_for
from werkzeug import Response
from ..controllers import process_file, get_clashes, role_required
from ..controllers import deny_override, allow_override, create_semester


admin_views = Blueprint("admin_views", __name__, template_folder="../templates")


@admin_views.route("/semester", methods=["GET"])
@role_required("Admin")
def get_upload_page() -> str:
    return render_template("semester.html")


@admin_views.route("/uploadFiles", methods=["GET"])
@role_required("Admin")
def get_uploadFiles_page() -> str:
    return render_template("uploadFiles.html")


@admin_views.route("/newSemester", methods=["POST"])
@role_required("Admin")
def new_semester_action() -> str:
    create_semester(
        request.form["teachingBegins"],
        request.form["teachingEnds"],
        int(request.form["semester"]),
        int(request.form["maxAssessments"]),
    )
    return render_template("uploadFiles.html")


@admin_views.route("/clashes", methods=["GET"])
@role_required("Admin")
def get_clashes_page() -> str:
    return render_template("clashes.html", exams=get_clashes())


@admin_views.route("/acceptOverride/<int:exam_id>", methods=["POST"])
@role_required("Admin")
def accept_override(exam_id: int) -> Response:
    allow_override(exam_id)
    return redirect(url_for("admin_views.get_clashes_page"))


@admin_views.route("/rejectOverride/<int:exam_id>", methods=["POST"])
@role_required("Admin")
def reject_override(exam_id: int) -> Response:
    deny_override(exam_id)
    return redirect(url_for("admin_views.get_clashes_page"))


@admin_views.route("/uploadcourse", methods=["POST"])
@role_required("Admin")
def upload_course_file() -> str | Response:
    file = request.files["file"]
    if file.filename == "":
        return render_template("uploadFiles.html", message="No file selected!")
    process_file(file)
    return redirect(url_for("course_views.get_courses_page"))
