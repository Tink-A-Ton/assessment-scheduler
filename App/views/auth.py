from flask import Blueprint, redirect, request, render_template, url_for
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    unset_jwt_cookies,
    set_access_cookies,
)
from flask.wrappers import Response
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.wrappers.response import Response
from App.models import User, Admin
from App.controllers.staff import create_staff
from App.controllers.user import is_admin

auth_views = Blueprint("auth_views", __name__, template_folder="../templates")


@auth_views.route("/login", methods=["GET"])
def get_login_page() -> str:
    return render_template("login.html")


@auth_views.route("/register", methods=["GET"])
def get_register_page() -> str:
    return render_template("signup.html")


@auth_views.route("/login", methods=["POST"])
def login_action() -> Response | str:
    data: ImmutableMultiDict[str, str] = request.form
    email: str | None = data.get("email")
    password: str | None = data.get("password")
    if not email or not password:
        return get_login_page()
    token: str | None = login_user(email, password)
    if not token:
        return get_login_page()
    redirect_url: str = (
        "admin_views.get_upload_page"
        if Admin.query.filter_by(email=email).first()
        else "staff_views.get_calendar_page"
    )
    response: Response = redirect(url_for(redirect_url))
    set_access_cookies(response, token)  # pyright: ignore[reportArgumentType]
    return response


@auth_views.route("/register", methods=["POST"])
def register_staff() -> Response | str:
    data: dict[str, str] = request.form
    staff_id: int = int(data["staffID"])
    firstname: str = data["firstName"]
    lastname: str = data["lastName"]
    position: str = data["status"]
    email: str = data["email"]
    password: str = data["password"]
    created: bool = create_staff(staff_id, email, password, firstname, lastname, position)
    if not created:
        return get_register_page()
    token: str | None = login_user(email, password)
    if not token:
        return get_login_page()
    response: Response = redirect(url_for("staff_views.get_calendar_page"))
    set_access_cookies(response, token)  # pyright: ignore[reportArgumentType]
    return response


@auth_views.route("/logout", methods=["GET"])
@jwt_required()
def logout() -> Response:
    response: Response = redirect(url_for("auth_views.get_login_page"))
    unset_jwt_cookies(response)  # pyright: ignore[reportArgumentType]
    return response


def login_user(email: str, password: str) -> str | None:
    user: User | None = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return create_access_token(identity=user.id)
    return None
