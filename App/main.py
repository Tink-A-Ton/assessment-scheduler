from flask import Flask, redirect, url_for
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .database import init_db
from .controllers import setup_jwt
from .config import load_config
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
    configure_uploads(app, photos)  # pyright: ignore[reportArgumentType]

    jwt: JWTManager = setup_jwt(app)

    @jwt.invalid_token_loader
    @jwt.unauthorized_loader
    def custom_unauthorized_response(error):
        return redirect(url_for("auth_views.get_login_page"))

    app.app_context().push()
    return app
