"""
Test the pytest-pylembic plugin functionality
"""

import shutil
import tempfile
from pathlib import Path

from pytest import fixture, Testdir


@fixture
def mock_migrations_dir():
    """Create a temporary directory with mock migration files."""
    temp_dir = tempfile.mkdtemp()
    migrations_dir = Path(temp_dir) / "migrations"
    migrations_dir.mkdir(exist_ok=True)

    # Create versions directory
    versions_dir = migrations_dir / "versions"
    versions_dir.mkdir(exist_ok=True)

    # Create basic alembic.ini
    with open(migrations_dir / "alembic.ini", "w") as f:
        f.write("[alembic]\nscript_location = migrations\n")

    # Create env.py
    with open(migrations_dir / "env.py", "w") as f:
        f.write("# Mock env.py file for testing\n")

    # Create a valid migration file
    with open(versions_dir / "1a2b3c4d5e6f_initial_migration.py", "w") as f:
        f.write("""
\"\"\"Initial migration

Revision ID: 1a2b3c4d5e6f
Revises:
Create Date: 2023-01-01 00:00:00.000000

\"\"\"
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '1a2b3c4d5e6f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
""")

    yield temp_dir

    # Cleanup
    shutil.rmtree(temp_dir)


@fixture
def mock_migrations_dir_multiple_heads():
    """Create a temporary directory with mock migration files with failure case."""
    temp_dir = tempfile.mkdtemp()
    migrations_dir = Path(temp_dir) / "migrations"
    migrations_dir.mkdir(exist_ok=True)

    # Create versions directory
    versions_dir = migrations_dir / "versions"
    versions_dir.mkdir(exist_ok=True)

    # Create basic alembic.ini
    with open(migrations_dir / "alembic.ini", "w") as f:
        f.write("[alembic]\nscript_location = migrations\n")

    # Create env.py
    with open(migrations_dir / "env.py", "w") as f:
        f.write("# Mock env.py file for testing\n")

    # Create two migration files with different heads (multiple heads)
    with open(versions_dir / "1a2b3c4d5e6f_initial.py", "w") as f:
        f.write("""
\"\"\"Initial migration

Revision ID: 1a2b3c4d5e6f
Revises:
Create Date: 2023-01-01 00:00:00.000000

\"\"\"
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '1a2b3c4d5e6f'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    pass

def downgrade():
    pass
""")
    with open(versions_dir / "2b3c4d5e6f7g_second_head.py", "w") as f:
        f.write("""
\"\"\"Second head

Revision ID: 2b3c4d5e6f7g
Revises:
Create Date: 2023-01-02 00:00:00.000000

\"\"\"
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '2b3c4d5e6f7g'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    pass

def downgrade():
    pass
""")

    yield temp_dir

    # Cleanup
    shutil.rmtree(temp_dir)


def test_plugin_registration(testdir: Testdir):
    """Test that the plugin is properly registered."""
    # Create a temporary pytest test file
    testdir.makepyfile("""
        def test_dummy():
            assert True
    """)

    # Run pytest with the plugin
    result = testdir.runpytest("--help")

    # Check that our options are in the help output
    result.stdout.fnmatch_lines(
        ["*pylembic*", "*--alembic-migrations-dir=*", "*--skip-pylembic*"]
    )


def test_migration_validation__verbose(testdir: Testdir, mock_migrations_dir: Path):
    """Test that the plugin correctly validates migrations."""
    # Create a temporary pytest test file
    testdir.makepyfile("""
        def test_dummy():
            assert True
    """)

    # Get the path to the mock migrations directory
    migrations_path = Path(mock_migrations_dir) / "migrations"

    # Run pytest with our plugin
    result = testdir.runpytest(
        f"--alembic-migrations-dir={migrations_path}", "--pylembic-verbose"
    )

    # The test collection should include our auto-generated test
    result.stdout.fnmatch_lines(
        [
            "*collected*",
            "*=== Pylembic migrations validation summary ===*",
            "*✨ Migrations validation successful ✨*",
        ]
    )


def test_failing_migration_multiple_heads(
    testdir: Testdir, mock_migrations_dir_multiple_heads: Path
):
    """Test that the plugin detects multiple heads and fails validation."""
    testdir.makepyfile("""
        def test_dummy():
            assert True
    """)
    migrations_path = Path(mock_migrations_dir_multiple_heads) / "migrations"
    result = testdir.runpytest(
        f"--alembic-migrations-dir={migrations_path}", "--pylembic-verbose"
    )
    # The dynamic test should fail and the summary should report failure
    result.stdout.fnmatch_lines(
        [
            "*collected*",
            "*=== Pylembic migrations validation summary ===*",
            "*❌ Migrations validation failed ❌*",
        ]
    )


def test_skip_validation(testdir: Testdir, mock_migrations_dir: Path):
    """Test that the plugin skips validation when requested."""
    # Create a temporary pytest test file
    testdir.makepyfile("""
        def test_dummy():
            assert True
    """)

    # Run pytest with skip option
    result = testdir.runpytest("--skip-pylembic")

    # Check that only our dummy test ran (not the alembic test)
    assert result.ret == 0

    # The plugin's summary should not be in the output
    assert "=== Pylembic migrations validation summary ===" not in result.stdout.str()
