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
pytest --pylembic-migrations-dir=path/to/migrations  # Specify a custom migrations directory
pytest --skip-pylembic                       # Skip migration validation
pytest --pylembic-detect-branches=False              # Disable branch detection
pytest --pylembic-verbose=False           # Disable verbose output
```

### ⚙️ Configuration in pytest.ini

You can also configure these options in your `pytest.ini` file:

```ini
[pytest]
addopts = --pylembic-migrations-dir=pylembic_migrations
```

## 🔍 Examples

### ▶️ Basic Usage

Simply run pytest as usual:

```bash
pytest
```

The plugin will automatically validate your migrations and report any issues.

### 🛠️ Custom Configuration

For a project with migrations in a non-standard location:

```bash
pytest --pylembic-migrations-dir=database/migrations
```

## ⚡ How It Works

This plugin leverages the `pylembic` library to perform validation on your Pylembic migrations. It automatically:

1. Adds a virtual test that runs before your other tests
2. Validates the migration files using the Validator class from pylembic
3. Reports any issues as test failures
4. Provides a summary of migration validation in the test report

## 📋 Requirements

- Python 3.11+
- pylembic

## 🪪 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

(c) 2025, Created with ❤️ by [Marco Espinosa](mailto:marco@marcoespinosa.com)
