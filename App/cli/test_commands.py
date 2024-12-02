import sys
import pytest
from flask import Flask
from flask.cli import AppGroup
from .utils import help_command, run_all_tests

test = AppGroup("test", help="Testing commands")


def create_cli_commands(app: Flask) -> None:

    @test.command("unit", help="Runs all Unit tests")
    def run_all_unit_tests() -> None:
        sys.exit(pytest.main(["-k", "UnitTests"]))

    @test.command("int", help="Runs all Integration tests")
    def run_all_integration_tests() -> None:
        sys.exit(pytest.main(["-k", "IntegrationTests"]))

    @test.command("all", help="Runs all tests (Unit and Integration)")
    def run_all_tests_cli() -> None:
        run_all_tests()

    app.cli.add_command(test)

    @app.cli.command("help", help="Displays all available commands and descriptions.")
    def help_command_cli() -> None:
        help_command(app, test)
