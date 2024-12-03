import sys
import pytest
from flask.cli import AppGroup

test = AppGroup("test", help="Testing commands")

@test.command("unit", help="Runs all Unit tests")
def run_all_unit_tests() -> None:
    sys.exit(pytest.main(["-k", "UnitTests"]))

@test.command("int", help="Runs all Integration tests")
def run_all_integration_tests() -> None:
    sys.exit(pytest.main(["-k", "IntegrationTests"]))

@test.command("all", help="Runs all tests (Unit and Integration)")
def run_all_tests_cli() -> None:
    run_all_tests()


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
