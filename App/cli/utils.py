import sys
import click
from flask import Flask
from flask.cli import AppGroup
import pytest
from rich.console import Console
from rich.table import Table


def help_command(app: Flask, test: AppGroup) -> None:
    ctx = click.Context(app.cli)
    groups: dict[str, AppGroup] = {"test": test}
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


def run_tests(test_type: str, unit_key: str, integration_key: str) -> None:
    if test_type == "unit":
        sys.exit(pytest.main(["-k", unit_key]))
    elif test_type == "int":
        sys.exit(pytest.main(["-k", integration_key]))
    else:
        unit_result: int | pytest.ExitCode = pytest.main(["-k", unit_key])
        if unit_result == 0:
            integration_result: int | pytest.ExitCode = pytest.main(
                ["-k", integration_key]
            )
            sys.exit(integration_result)
        else:
            sys.exit(unit_result)


def run_all_tests() -> None:
    unit_result: int | pytest.ExitCode = pytest.main(["-k", "UnitTests"])
    if unit_result == 0:
        integration_result: int | pytest.ExitCode = pytest.main(
            ["-k", "IntegrationTests"]
        )
        sys.exit(integration_result)
    else:
        sys.exit(unit_result)
