from flask import Blueprint, render_template

course_views = Blueprint("course_views", __name__, template_folder="../templates")


@course_views.route("/courses", methods=["GET"])
def index() -> str:
    return render_template("courses.html")
