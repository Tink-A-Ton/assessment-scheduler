# this is the root or the endpoint; the other files export an AppGroup
import click
from flask import Flask
from flask.cli import AppGroup
from rich.console import Console
from rich.table import Table
from .test import test
from .exam import exam
from .course import course
from .staff import staff


def create_cli_commands(app: Flask) -> None:
    app.cli.add_command(test)
    app.cli.add_command(exam)
    app.cli.add_command(course)
    app.cli.add_command(staff)

    @app.cli.command("help", help="Displays all available commands and descriptions.")
    def help_command_cli() -> None:
        help_command(app)


def help_command(app: Flask) -> None:
    ctx = click.Context(app.cli)
    groups: dict[str, AppGroup] = {"test": test, "exam": exam, "course": course, "staff": staff}
    table = Table(title="Available Commands")
    table.add_column("Command", justify="left", style="cyan", no_wrap=True)
    table.add_column("Description", justify="left", style="magenta")
    for cmd in app.cli.list_commands(ctx):
        command: click.Command | None = app.cli.get_command(ctx, cmd)
        table.add_row(cmd, command.help if command else "No description available")
    for group_name, group in groups.items():
        for cmd in group.list_commands(ctx):
            command = group.get_command(ctx, cmd)
            table.add_row(
                f"{group_name} {cmd}",
                command.help if command else "No description available",
            )
    console = Console()
    console.print(table)