from typing import Optional
from flask import Blueprint, redirect, request, render_template, url_for
from flask_jwt_extended import jwt_required, unset_jwt_cookies, set_access_cookies
from flask.wrappers import Response
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.wrappers.response import Response
from ..controllers import create_staff, login_user, is_admin_account
from ..database import db

auth_views = Blueprint("auth_views", __name__, template_folder="../templates")


@auth_views.route("/login", methods=["GET"])
def get_login_page() -> str:
    return render_template("login.html")


@auth_views.route("/register", methods=["GET"])
def get_register_page() -> str:
    return render_template("register.html")


@auth_views.route("/login", methods=["POST"])
def login_action() -> Response | str:
    try:
        data: ImmutableMultiDict[str, str] = request.form
        email: Optional[str] = data.get("email")
        password: Optional[str] = data.get("password")
        if not email or not password:
            return get_login_page()
        token: Optional[str] = login_user(email, password)
        if not token:
            return get_login_page()
        redirect_url: str = (
            "admin_views.get_upload_page"
            if is_admin_account(email)
            else "staff_views.get_calendar_page"
        )
        response: Response = redirect(url_for(redirect_url))
        set_access_cookies(response, token)  # pyright: ignore
        return response
    except Exception:
        db.session.rollback()
        return get_login_page()


@auth_views.route("/register", methods=["POST"])
def register_staff() -> Response | str:
    try:
        data: dict[str, str] = request.form
        created: bool = create_staff(
            int(data["staffID"]),
            data["email"],
            data["password"],
            data["firstName"],
            data["lastName"],
            data["status"],
        )
        if not created:
            return get_register_page()
        token: Optional[str] = login_user(data["email"], data["password"])
        if not token:
            return get_login_page()
        response: Response = redirect(url_for("staff_views.get_calendar_page"))
        set_access_cookies(response, token)  # pyright: ignore
        return response
    except Exception:
        db.session.rollback()
        return get_login_page()


@auth_views.route("/logout", methods=["GET"])
@jwt_required()
def logout() -> Response:
    try:
        response: Response = redirect(url_for("auth_views.get_login_page"))
        unset_jwt_cookies(response)  # pyright: ignore
        return response
    except Exception:
        return response
