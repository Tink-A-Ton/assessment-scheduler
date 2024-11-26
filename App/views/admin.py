from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_jwt_extended import jwt_required
from App.models import Admin
from App.database import db
from werkzeug.utils import secure_filename
import os, csv
from datetime import datetime
from App.models.course import Course
from App.controllers.course import add_course, get_all_courses, get_course, delete_course, edit_course
from App.controllers.semester import add_semester
from App.controllers.assessment import get_assessment_by_id
from flask_jwt_extended import get_jwt_identity

from App.models.courseAssessment import CourseAssessment

admin_views = Blueprint("admin_views", __name__, template_folder="../templates")


# Gets Semester Details Page
@admin_views.route("/semester", methods=["GET"])
@jwt_required(Admin)
def get_upload_page():
    return render_template("semester.html")


@admin_views.route("/uploadFiles", methods=["GET"])
@jwt_required(Admin)
def get_uploadFiles_page():
    return render_template("uploadFiles.html")


# Gets Course Listings Page
@admin_views.route("/coursesList", methods=["GET"])
@jwt_required(Admin)
def index():
    return render_template("courses.html")


# Retrieves semester details and stores it in global variables
@admin_views.route("/newSemester", methods=["POST"])
@jwt_required(Admin)
def new_semester_action():
    semBegins = request.form.get("teachingBegins")
    semEnds = request.form.get("teachingEnds")
    semChoice = request.form.get("semester")
    maxAssessments = request.form.get(
        "maxAssessments"
    )
    add_semester(semBegins, semEnds, semChoice, maxAssessments)
    return render_template("uploadFiles.html")


# Gets csv file with course listings, parses it to store course data and stores it in application
@admin_views.route("/uploadcourse", methods=["POST"])
@jwt_required(Admin)
def upload_course_file():
    file = request.files["file"]

    # Check if file is present
    if file.filename == "":
        message = "No file selected!"
        return render_template("uploadFiles.html", message=message)
    else:
        filename = secure_filename(file.filename)
        file.save(os.path.join("App/uploads", filename))
        fpath = "App/uploads/" + filename
        with open(fpath, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                add_course(
                    course_code=row["Course Code"],
                    course_title=row["Course Title"],
                    level=int(row["Level"]),
                    semester=int(row["Semester"]),
                )
    return redirect(url_for("admin_views.get_courses"))


# Pull course list from database
@admin_views.route("/get_courses", methods=["GET"])
@jwt_required(Admin)
def get_courses():
    courses: list[Course] = get_all_courses()
    print(courses)
    return render_template("courses.html", courses=courses)


# Gets Add Course Page
@admin_views.route("/newCourse", methods=["GET"])
@jwt_required(Admin)
def get_new_course():
    return render_template("addCourse.html")


# Retrieves course info and stores it in database ie. add new course
@admin_views.route("/addNewCourse", methods=["POST"])
@jwt_required(Admin)
def add_course_action():
    course_code = request.form.get("course_code")
    title = request.form.get("title")
    description = request.form.get("description")
    data = request.form
    level = request.form.get("level")
    semester = request.form.get("semester")
    numAssessments = request.form.get("numAssessments")

    course = add_course(
        course_code=course_code, course_title=title, level=level, semester=semester
    )

    # Redirect to view course listings!
    return redirect(url_for("admin_views.get_courses"))


# Gets Update Course Page
@admin_views.route("/modifyCourse/<string:course_code>", methods=["GET"])
@jwt_required(Admin)
def get_update_course(course_code):
    course = get_course(course_code)  # Gets selected course
    return render_template("updateCourse.html", course=course)


# Selects new course details and updates existing course in database
@admin_views.route("/updateCourse", methods=["POST"])
@jwt_required(Admin)
def update_course():
    course_code: str | None = request.form.get("code")
    title: str | None = request.form.get("title")
    description: str | None = request.form.get("description")
    level: str | None = request.form.get("level")
    semester: str | None = request.form.get("semester")
    num_assessments: str | None = request.form.get("assessment")
    # programme = request.form.get('programme')

    delete_course(course_code=course_code)
    edit_course(course_code=course_code, course_title=title, level=level, semester_id=semester)
    flash("Course Updated Successfully!")

    # Redirect to view course listings!
    return redirect(url_for("admin_views.get_courses"))


# Selects course and removes it from database
@admin_views.route("/deleteCourse/<string:course_code>", methods=["POST"])
@jwt_required(Admin)
def delete_course_action(course_code):
    delete_course(course_code)
    print(course_code, " deleted")
    flash("Course Deleted Successfully!")

    # Redirect to view course listings!
    return redirect(url_for("admin_views.get_courses"))


# @admin_views.route("/clashes", methods=["GET"])
# @jwt_required(Admin)
# def get_clashes_page():
#     # for search
#     all_assessments = CourseAssessment.query.all()
#     start_date = request.args.get("start_date")
#     end_date = request.args.get("end_date")
#     searchResults = []
#     if start_date and end_date:
#         start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
#         end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
#         for a in all_assessments:
#             if (
#                 start_date <= a.startDate <= end_date
#                 or start_date <= a.endDate <= end_date
#             ):
#                 searchResults.append(a)
#     # for table
#     assessments = get_clashes()
#     return render_template(
#         "clashes.html", assessments=assessments, results=searchResults
#     )


@admin_views.route("/acceptOverride/<int:assessment_id>", methods=["POST"])
@jwt_required(Admin)
def accept_override(assessment_id):
    assessment: CourseAssessment | None = get_assessment_by_id(assessment_id)
    if assessment:
        assessment.clash_detected = False
        db.session.commit()
        print("Accepted override.")
    return redirect(url_for("admin_views.get_clashes_page"))


@admin_views.route("/rejectOverride/<int:assessment_id>", methods=["POST"])
@jwt_required(Admin)
def reject_override(assessment_id):
    assessment: CourseAssessment | None = get_assessment_by_id(assessment_id)
    if assessment:
        assessment.clash_detected = False
        assessment.start_date = None
        assessment.end_date = None
        assessment.start_time = None
        assessment.end_time = None
        db.session.commit()
        print("Rejected override.")
    return redirect(url_for("admin_views.get_clashes_page"))
