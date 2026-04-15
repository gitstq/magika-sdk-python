# Contributing to Magika SDK Python

Thank you for your interest in contributing to Magika SDK Python! 🎉

This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How Can I Contribute?

### Reporting Bugs

- Use the [GitHub Issues](https://github.com/gitstq/magika-sdk-python/issues) to report bugs
- Include detailed information:
  - Python version
  - Operating system
  - Steps to reproduce
  - Expected vs actual behavior
  - Error messages if applicable

### Suggesting Features

- Use [GitHub Issues](https://github.com/gitstq/magika-sdk-python/issues) to suggest features
- Provide clear use cases and examples
- Explain why this feature would be beneficial

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/AmazingFeature`
3. Make your changes
4. Run tests: `pytest tests/ -v`
5. Commit with clear messages: `git commit -m 'Add some AmazingFeature'`
6. Push to your branch: `git push origin feature/AmazingFeature`
7. Open a Pull Request

## Commit Message Format

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Build or tool changes

### Examples

```
feat(core): add async batch processing support

Adds AsyncMagikaScanner class for high-performance concurrent file scanning
with progress tracking and configurable worker pools.

fix(security): resolve false positive in threat detection

Corrects threat level classification for Python source files.
```

## Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/magika-sdk-python.git
cd magika-sdk-python

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Format code
black magika_sdk/ tests/
isort magika_sdk/ tests/

# Type checking
mypy magika_sdk/
```

## Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type annotations for all function signatures
- Write docstrings for all public modules, functions, and classes
- Maximum line length: 100 characters

## Testing

- Write tests for all new features
- Ensure all tests pass before submitting PR
- Aim for high test coverage

```bash
# Run tests with coverage
pytest tests/ -v --cov=magika_sdk --cov-report=html

# View coverage report
open htmlcov/index.html
```

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
