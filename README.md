# AG-UI Agent MCP

An example of creating an agent with access to MCP (Model Context Protocol) tools, deployed on Foundry, that exposes the AG-UI protocol. This project demonstrates how to build intelligent agents that can interact with various tools and services through standardized protocols.

## Overview

This repository provides a reference implementation for building agents that:
- Utilize the Model Context Protocol (MCP) for tool integration
- Expose the AG-UI protocol for agent interaction
- Deploy seamlessly on Palantir Foundry
- Are built with Python for ease of development and deployment

## Features

- **MCP Tool Integration**: Access to a wide range of tools through the Model Context Protocol
- **AG-UI Protocol**: Standardized agent-to-UI communication interface
- **Foundry Deployment**: Ready for deployment on Palantir Foundry platform
- **Python-based**: Leverages Python's rich ecosystem for AI/ML development
- **Extensible Architecture**: Easy to add new tools and capabilities

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package installer)
- Git
- Virtual environment tool (venv or virtualenv)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/jspoelstra/ag-ui-agent-mcp.git
cd ag-ui-agent-mcp
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

(Usage instructions will be added as the project develops)

```python
# Example usage code will be provided here
```

## Architecture

This project follows a modular architecture:

- **Agent Core**: Main agent logic and orchestration
- **MCP Integration**: Handles communication with MCP tools
- **AG-UI Protocol**: Implements the AG-UI protocol for UI interactions
- **Foundry Deployment**: Configuration and utilities for Foundry deployment

## Contributing

We welcome contributions from the community! Please read our contributing guidelines below to get started.

### How to Contribute

1. **Fork the Repository**
   - Click the "Fork" button at the top right of this repository
   - Clone your fork locally:
     ```bash
     git clone https://github.com/YOUR_USERNAME/ag-ui-agent-mcp.git
     cd ag-ui-agent-mcp
     ```

2. **Set Up Your Development Environment**
   - Follow the installation instructions above
   - Create a new branch for your feature or fix:
     ```bash
     git checkout -b feature/your-feature-name
     ```

3. **Make Your Changes**
   - Write clear, concise code that follows the project's coding standards
   - Add or update tests as needed
   - Update documentation to reflect your changes

4. **Test Your Changes**
   - Run the test suite to ensure nothing is broken:
     ```bash
     pytest
     ```
   - Run linting and formatting checks:
     ```bash
     ruff check .
     black --check .
     ```

5. **Commit Your Changes**
   - Write clear, descriptive commit messages:
     ```bash
     git add .
     git commit -m "Add feature: description of your changes"
     ```

6. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Select your fork and branch
   - Provide a clear description of your changes
   - Link any related issues

### Development Guidelines

#### Code Style

This project follows Python best practices and PEP 8 style guidelines:

- Use meaningful variable and function names
- Write docstrings for all classes and functions
- Keep functions small and focused
- Maximum line length: 100 characters
- Use type hints where appropriate

We use the following tools to maintain code quality:
- **Black**: Code formatting
- **Ruff**: Fast Python linter
- **MyPy**: Static type checking

#### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_agent.py
```

#### Code Formatting

```bash
# Format code with Black
black .

# Check formatting without making changes
black --check .

# Sort imports
isort .
```

#### Linting

```bash
# Run Ruff linter
ruff check .

# Auto-fix issues where possible
ruff check --fix .

# Run type checking
mypy .
```

### Reporting Issues

If you find a bug or have a suggestion:

1. Check if the issue already exists in the [Issues](https://github.com/jspoelstra/ag-ui-agent-mcp/issues) section
2. If not, create a new issue with:
   - A clear, descriptive title
   - Detailed description of the problem or suggestion
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Your environment details (OS, Python version, etc.)

### Pull Request Guidelines

- Keep pull requests focused on a single feature or fix
- Update the README.md if you add functionality
- Add tests for new features
- Ensure all tests pass
- Update documentation as needed
- Follow the existing code style
- Write clear commit messages

### Code Review Process

1. All pull requests require review from at least one maintainer
2. Address any feedback or requested changes
3. Once approved, a maintainer will merge your PR
4. Your contribution will be credited in the project

## Development Setup

For contributors working on the project:

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Set up pre-commit hooks
pre-commit install

# Run pre-commit checks manually
pre-commit run --all-files
```

## Testing

This project uses pytest for testing. Tests are located in the `tests/` directory.

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_agent.py::test_function_name

# Generate coverage report
pytest --cov=. --cov-report=term-missing
```

## Deployment

(Deployment instructions for Foundry will be added here)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Model Context Protocol (MCP) community
- AG-UI Protocol contributors
- Palantir Foundry platform

## Contact

- **Author**: Jacob Spoelstra
- **Repository**: [https://github.com/jspoelstra/ag-ui-agent-mcp](https://github.com/jspoelstra/ag-ui-agent-mcp)

## Project Status

This project is currently in active development. Contributions and feedback are welcome!

---

For more information about:
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [AG-UI Protocol](https://github.com/topics/ag-ui)
- [Palantir Foundry](https://www.palantir.com/platforms/foundry/)
