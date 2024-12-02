from datetime import timedelta
from os import getenv
import time
from dotenv import load_dotenv
from flask import Flask, redirect, url_for
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from werkzeug import Response
from .database import init_db
from .controllers import setup_jwt
from .views import views
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads


def add_views(app) -> None:
    for view in views:
        app.register_blueprint(view)


def create_app(overrides={}) -> Flask:
    app = Flask(__name__, static_url_path="/static")
    load_config(app, overrides)
    CORS(app)
    add_views(app)
    init_db(app)
    photos = UploadSet("photos", TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)  # pyright: ignore

    jwt: JWTManager = setup_jwt(app)

    @jwt.invalid_token_loader
    @jwt.unauthorized_loader
    def custom_unauthorized_response(error) -> Response:
        return redirect(url_for("auth_views.get_login_page"))

    app.app_context().push()
    return app


def load_config(app: Flask, overrides) -> None:
    load_dotenv()
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SECRET_KEY"] = getenv("SECRET_KEY")
    app.config["DEBUG"] = app.config["ENV"].upper() != "PRODUCTION"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
        hours=int(getenv("JWT_ACCESS_TOKEN_EXPIRES", default=15))
    )
    app.config["MAIL_DEFAULT_SENDER"] = getenv("MAIL_DEFAULT_SENDER")
    app.config["JWT_ACCESS_COOKIE_NAME"] = getenv("JWT_ACCESS_COOKIE_NAME")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["PREFERRED_URL_SCHEME"] = "https"
    app.config["UPLOADED_PHOTOS_DEST"] = "App/uploads"
    app.config["JWT_TOKEN_LOCATION"] = ["cookies", "headers"]
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 465
    app.config["MAIL_USE_TLS"] = True
    app.config["JWT_COOKIE_SECURE"] = True
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    for key in overrides:
        app.config[key] = overrides[key]