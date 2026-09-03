<!-- Shields -->
<p align="center">
<a href="https://github.com/maekind/pytest-pylembic"><img src="https://img.shields.io/github/actions/workflow/status/maekind/pytest-pylembic/.github%2Fworkflows%2Ftesting.yaml?label=tests&color=green" hspace="5"></a>
<a href="https://github.com/maekind/pytest-pylembic/releases"><img src="https://img.shields.io/github/actions/workflow/status/maekind/pytest-pylembic/.github%2Fworkflows%2Frelease.yaml?label=build%20package&color=green" hspace="5"></a>
<a href="https://pypi.org/project/pytest-pylembic"><img src="https://img.shields.io/github/v/release/maekind/pytest-pylembic?color=blue&label=pypi" hspace="5"></a>
<br>
<a href="https://github.com/maekind/pytest-pylembic/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-orange.svg" hspace="5"></a>
<a href="https://github.com/maekind/pytest-pylembic"><img src="https://img.shields.io/github/repo-size/maekind/pytest-pylembic?color=red" hspace="5"></a>
<a href="https://github.com/maekind/pytest-pylembic"><img src="https://img.shields.io/github/last-commit/maekind/pytest-pylembic?color=black" hspace="5"></a>
<a href="https://www.python.org/downloads/"><img src="https://img.shields.io/github/languages/top/maekind/pytest-pylembic?color=darkgreen" hspace="5"></a>
<a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python%20version-%3E3.11-lightblue" hspace="5"></a>
</p>
<!-- End of Shields -->

# 🧪 pytest-pylembic

A pytest plugin for validating Pylembic database migrations automatically.

## 📝 Overview

`pytest-pylembic` is a pytest plugin that integrates with `pylembic` to automatically validate your Pylembic database migrations during test runs. This plugin makes it easy to ensure your migration files:

- Have no duplicate revision IDs
- Maintain a linear history (or properly branched history)
- Correctly define dependencies between migrations
- Follow proper formatting conventions

## 📦 Installation

```bash
pip install pytest-pylembic
```

## ⚙️ Usage

Once installed, the plugin automatically runs migration validation when you execute `pytest`. No additional configuration is required if your migrations are in the standard `migrations` directory.

### 💻 Command Line Options

You can customize the plugin's behavior with these pytest command line options:

```bash
pytest --alembic-migrations-dir=path/to/migrations  # Specify a custom migrations directory
pytest --skip-pylembic                              # Skip migration validation
pytest --pylembic-detect-branches=False             # Disable branch detection
pytest --pylembic-verbose=False                     # Disable verbose output
```

### ⚙️ Configuration in pytest.ini

You can also configure these options in your `pytest.ini` file:

```ini
[pytest]
addopts = --alembic-migrations-dir=alembic_migrations_dir --pylembic-detect-branches=False --pylembic-verbose
```

## 🐍 Configuration in pyproject.toml

You can also configure these options in your `pyproject.toml` file:

```toml
[tool.pytest.ini_options]
addopts = "--alembic-migrations-dir=alembic_migrations_dir --pylembic-detect-branches=False --pylembic-verbose"
```

## 🔍 Examples

### ▶️ Basic Usage

Simply run pytest as usual:

```bash
addopts = --alembic-migrations-dir=alembic_migrations_dir --pylembic-detect-branches=False --pylembic-verbose
```

## 🔍 Examples

### ▶️ Basic Usage

Simply run pytest as usual:

```bash
> pytest

===================================================================================================== test session starts ======================================================================================================
platform darwin -- Python 3.14.0, pytest-9.1.1, pluggy-1.6.0
rootdir: /whatever_is_your_root_project
configfile: pyproject.toml
plugins: pylembic-0.4.0
collected 0 items                                                                                                                                                                                                              

.venv/lib/python3.14/site-packages/pytest_pylembic/plugin.py .                                                                                                                                                           [100%]

============================================================================================ Pylembic migrations validation summary ============================================================================================
INFO     pylembic.logger:validator.py:158 No branching migrations detected.
INFO     pylembic.logger:validator.py:95 Only one migration detected. Skipping orphan check.
INFO     pylembic.logger:validator.py:125 No multiple bases or heads detected.

✨ Migrations validation successful ✨
======================================================================================== End of Pylembic migrations validation summary =========================================================================================
====================================================================================================== 1 passed in 0.17s =======================================================================================================

```

The plugin will automatically validate your migrations and report any issues.

### 🛠️ Custom Configuration

For a project with migrations in a non-standard location:

```bash
pytest --alembic-migrations-dir=database/migrations
```

## ⚡ How It Works

This plugin leverages the `pylembic` library to perform validation on your Pylembic migrations. It automatically:

1. Adds a virtual test that runs before your other tests
2. Validates the migration files using the Validator class from pylembic
3. Reports any issues as test failures
4. Provides a summary of migration validation in the test report

## 📋 Requirements

- Python 3.11+
- [Pylembic](https://pypi.org/project/pylembic/)

## 🪪 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

(c) 2025-2026, Created with ❤️ by [Marco Espinosa](mailto:marco@marcoespinosa.com)
