from flask import Flask
from flask_migrate import Migrate
from App.database import get_migrate
from App.main import create_app
from App.controllers import initialize
from App.cli import create_cli_commands

app: Flask = create_app()
migrate: Migrate = get_migrate(app)
create_cli_commands(app)


@app.cli.command("init", help="Creates and initializes the database")
def init() -> None:
    initialize()
    print("Database initialized")
