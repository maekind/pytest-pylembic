"""
pytest plugin for testing Alembic migrations using pylembic
"""

import os
from pathlib import Path

from _pytest.terminal import TerminalReporter
from pytest import Config, Function, Module, Parser, Session, mark
from pylembic.validator import Validator


def pytest_addoption(parser: Parser) -> None:
    """Add pytest_pylembic options to pytest command line."""
    group = parser.getgroup("pylembic")
    group.addoption(
        "--alembic-migrations-dir",
        action="store",
        default="migrations",
        help="Path to the alembic's migrations directory. Default: 'migrations'",
    )
    group.addoption(
        "--skip-pylembic", action="store_true", help="Skip pylembic validation"
    )
    group.addoption(
        "--pylembic-detect-branches",
        action="store_true",
        default=True,
        help="Detect migration branches. Default: True",
    )
    group.addoption(
        "--pylembic-verbose",
        action="store_true",
        default=False,
        help="Show verbose output for pylembic validation. Default: False",
    )


def pytest_configure(config: Config) -> None:
    """Register the plugin marker."""
    config.addinivalue_line(
        "markers", "pylembic: mark test as a pylembic migration test"
    )


def pytest_collection_modifyitems(
    session: Session, config: Config, items: list[Function]
) -> None:
    """Add pylembic tests to the test collection."""
    # Skip if explicitly disabled
    if config.getoption("--skip-pylembic"):
        return

    # Get options
    migrations_dir = config.getoption("--alembic-migrations-dir")
    detect_branches = config.getoption("--pylembic-detect-branches")
    verbose = config.getoption("--pylembic-verbose")

    # Get absolute path to migrations directory
    base_path = Path(os.getcwd())
    migrations_path = base_path / migrations_dir

    if not migrations_path.exists():
        # Skip test creation if migrations directory doesn't exist
        return

    # Create the test function
    @mark.pylembic
    def test_pylembic_migrations():
        """Test migrations using pylembic."""
        migration_validator = Validator(str(migrations_path))
        assert migration_validator.validate(
            verbose=verbose, detect_branches=detect_branches
        )

    # Add the test to the collection. When no other tests were collected
    # there is no sibling item to borrow a parent from, so fall back to a
    # synthetic module. A bare Session as parent would also work but
    # pytest's getmodpath() only stops walking up the tree at a Module
    # ancestor, so without one the computed node name gains a stray
    # leading dot (".test_pylembic_migrations"), which breaks the
    # head_line match in pytest_terminal_summary below.
    if items:
        parent = items[0].parent
    else:
        parent = Module.from_parent(session, path=Path(__file__))

    test_item = Function.from_parent(
        name="test_pylembic_migrations",
        parent=parent,
        callobj=test_pylembic_migrations,
    )

    if test_item:
        items.insert(0, test_item)


def pytest_terminal_summary(
    terminalreporter: TerminalReporter, exitstatus: int, config: Config
) -> None:
    """Add a summary of pylembic migration tests to the terminal output."""
    if not config.getoption("--skip-pylembic"):
        tr = terminalreporter
        tr.write_sep("=", "Pylembic migrations validation summary")

        if not config.getoption("--pylembic-verbose"):
            tr.write_line(
                "Enable verbose mode with --pylembic-verbose for more details."
            )

        pylembic_passed = 0
        for passed in tr.stats.get("passed", []):
            if (
                hasattr(passed, "head_line")
                and passed.head_line == "test_pylembic_migrations"
            ):
                pylembic_passed += 1
                if hasattr(passed, "caplog"):
                    tr.write_line(passed.caplog)

        if pylembic_passed:
            tr.write_line("\n✨ Migrations validation successful ✨")
        else:
            for failed in tr.stats.get("failed", []):
                if (
                    hasattr(failed, "head_line")
                    and failed.head_line == "test_pylembic_migrations"
                ):
                    tr.write_line("\n❌ Migrations validation failed ❌")
                    if hasattr(failed, "caplog"):
                        tr.write_line(failed.caplog)

        tr.write_sep("=", "End of Pylembic migrations validation summary")
