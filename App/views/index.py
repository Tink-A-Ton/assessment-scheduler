from flask import Blueprint, render_template, request
from flask_jwt_extended import jwt_required
from ..controllers import initialize
from flask_mail import Mail, Message
from flask import current_app


index_views = Blueprint("index_views", __name__, template_folder="../templates")

@index_views.route("/settings", methods=["GET"])
@jwt_required()
def get_settings_page() -> str:
    return render_template("settings.html")


@index_views.route("/send_email", methods=["GET", "POST"])
def send_email() -> str:
    mail = Mail(current_app)  # Create mail instance
    subject = "Test Email!"
    receiver: str = request.form["email"]
    body = "Successful Registration"
    msg = Message(subject, recipients=[receiver], html=body)
    mail.send(msg)
    return render_template("login.html")
