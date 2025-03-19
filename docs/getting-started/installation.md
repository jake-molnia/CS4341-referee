# Installation

## Prerequisites

Before installing the CS4341 Game Referee, ensure you have the following:

- **Python 3.10 or higher** ([Check your Python version](../checking-python-version.md))
- **pip package manager** ([Check pip installation](../checking-pip.md))
- **git** ([Check git installation](../checking-git.md))

## Installing from GitHub

The recommended way to install the referee is directly from GitHub:

```bash
pip install git+https://github.com/jake-molnia/cs4341-referee.git
```

This will install the referee and all its dependencies.

## Development Installation

If you plan to contribute to the referee or customize it for your own needs, you can install it in development mode:

```bash
# Clone the repository
git clone https://github.com/jake-molnia/cs4341-referee.git
cd cs4341-referee

# Install in development mode with dev dependencies
pip install -e ".[dev]"
```

This installs the package in "editable" mode, allowing you to modify the code and see changes immediately without reinstalling.

## Verifying Installation

After installation, verify that the referee is properly installed by checking its version:

```bash
cs4341-referee --version
```

You should see output showing the current version of the referee.

## Dependencies

The referee has the following dependencies:

- **click**: Command-line interface toolkit
- **colorama**: Terminal color output
- **flask**: Web server for visualization
- **flask-cors**: Cross-origin resource sharing support
- **waitress**: Production WSGI server
- **toml**: Configuration file parsing

For development:

- **pytest**: Testing framework
- **pytest-cov**: Test coverage
- **black**: Code formatting
- **isort**: Import sorting
- **mypy**: Type checking
- **pre-commit**: Git hooks

## Troubleshooting

If you encounter any issues during installation:

### Common Issues

1. **Python version error**:
   Make sure you have Python 3.10 or higher installed. Check with `python --version` or `python3 --version`.

2. **Permission errors**:
   You might need to use `pip install --user` or consider using a virtual environment.

3. **Missing dependencies**:
   If you see errors about missing packages, try running:

   ```bash
   pip install --upgrade pip
   pip install git+https://github.com/jake-molnia/cs4341-referee.git
   ```

4. **Command not found**:
   Ensure that the Python scripts directory is in your PATH. You might need to restart your terminal after installation.

If issues persist, check the project's GitHub issues or contact the course staff for assistance.
