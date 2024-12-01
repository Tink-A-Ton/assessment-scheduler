import os
from datetime import timedelta
from flask import Flask


def load_config(app: Flask, overrides) -> None:
    config: dict = {"ENV": os.environ.get("ENV", "DEVELOPMENT")}
    if config["ENV"] == "DEVELOPMENT":
        from .default_config import (
            SQLALCHEMY_DATABASE_URI,
            SECRET_KEY,
        )

        app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
        app.config["SECRET_KEY"] = SECRET_KEY
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
        app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
        app.config["DEBUG"] = app.config["ENV"].upper() != "PRODUCTION"

    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=int(7))
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["PREFERRED_URL_SCHEME"] = "https"
    app.config["UPLOADED_PHOTOS_DEST"] = "App/uploads"
    app.config["JWT_TOKEN_LOCATION"] = ["cookies", "headers"]
    # app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 465
    app.config["MAIL_USERNAME"] = "assessment.scheduler.emails@gmail.com"
    app.config["MAIL_PASSWORD"] = "mygl qlni lqrz naxm"  # App Password used
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_DEFAULT_SENDER"] = "assessment.scheduler.emails@gmail.com"
    app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token"
    app.config["JWT_COOKIE_SECURE"] = True
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    # app.config["DEBUG"] = True
    for key in overrides:
        app.config[key] = overrides[key]
