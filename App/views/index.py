from flask import Blueprint, request, jsonify, render_template
from App.controllers.initialize import initialize

index_views = Blueprint("index_views", __name__, template_folder="../templates")


@index_views.route("/", methods=["GET"])
def index() -> str:
    return render_template("login.html")


@index_views.route("/init", methods=["GET"])
def init() -> dict[str, str]:
    initialize()
    return {"message": "Objects created"}
