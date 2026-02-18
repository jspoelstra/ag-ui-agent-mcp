# Contributing to AG-UI Agent with MCP

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Submitting Changes](#submitting-changes)
- [Coding Standards](#coding-standards)

## Code of Conduct

This project follows the Microsoft Open Source Code of Conduct. By participating, you are expected to uphold this code.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Create a new branch for your feature or bugfix
4. Make your changes
5. Test your changes
6. Submit a pull request

## Development Setup

### Prerequisites
- Python 3.11+
- Azure CLI
- Git

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/ag-ui-agent-mcp.git
cd ag-ui-agent-mcp

# Run quick start
./quickstart.sh

# Or manually:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Environment Configuration

```bash
cp .env.example .env
# Edit .env with your configuration
```

## Making Changes

### Branch Naming

Use descriptive branch names:
- `feature/add-new-tool` - for new features
- `fix/connection-error` - for bug fixes
- `docs/improve-readme` - for documentation updates
- `refactor/simplify-agent` - for code refactoring

### Code Style

This project follows Python best practices:

1. **Type Hints**: Use type hints for function parameters and return values
   ```python
   def create_agent(name: str, model: str) -> Agent:
       ...
   ```

2. **Docstrings**: Use docstrings for all public functions and classes
   ```python
   def deploy_agent():
       """
       Deploy the agent to Azure Foundry platform.
       
       Returns:
           bool: True if deployment successful, False otherwise
       """
   ```

3. **Formatting**: Follow PEP 8 guidelines
   - 4 spaces for indentation
   - 79 characters max line length for code
   - 72 characters max for docstrings/comments

4. **Imports**: Group imports in standard order
   ```python
   # Standard library
   import asyncio
   import os
   
   # Third-party
   from dotenv import load_dotenv
   from fastapi import FastAPI
   
   # Local
   from agent_framework import Agent
   ```

### Testing Your Changes

1. **Syntax Check**
   ```bash
   python -m py_compile agent.py
   ```

2. **Local Testing**
   ```bash
   python agent.py
   # In another terminal:
   python test_client.py
   ```

3. **Docker Testing**
   ```bash
   docker-compose up --build
   ```

### Commit Messages

Write clear, descriptive commit messages:

**Good:**
```
Add support for multiple MCP servers

- Allow configuration of multiple MCP endpoints
- Update documentation with examples
- Add tests for multi-server setup
```

**Bad:**
```
fix stuff
```

**Format:**
- First line: Brief summary (50 chars or less)
- Blank line
- Detailed explanation if needed
- List of changes with bullet points

## Submitting Changes

### Pull Request Process

1. **Update Documentation**
   - Update README.md if you changed functionality
   - Update USAGE.md if you changed usage patterns
   - Add comments to complex code

2. **Test Your Changes**
   - Ensure the agent runs without errors
   - Test with different configurations
   - Verify Docker build works

3. **Create Pull Request**
   - Push your branch to your fork
   - Open a PR against the main repository
   - Fill out the PR template completely

4. **PR Description Should Include:**
   - What changes were made and why
   - How to test the changes
   - Screenshots (if UI changes)
   - Related issue numbers

### PR Review Process

- Maintainers will review your PR
- Address any requested changes
- Once approved, your PR will be merged

## Coding Standards

### Python Best Practices

1. **Error Handling**
   ```python
   try:
       result = await dangerous_operation()
   except SpecificException as e:
       logger.error(f"Operation failed: {e}")
       raise
   ```

2. **Async/Await**
   ```python
   async def fetch_data():
       async with session.get(url) as response:
           return await response.json()
   ```

3. **Environment Variables**
   ```python
   # Use defaults for non-sensitive config
   port = int(os.getenv("PORT", "8000"))
   
   # Require critical configuration
   api_key = os.getenv("API_KEY")
   if not api_key:
       raise ValueError("API_KEY must be set")
   ```

### Security Guidelines

1. **Never Commit Secrets**
   - Use .env files (already in .gitignore)
   - Use environment variables
   - Use Azure Key Vault for production

2. **Input Validation**
   ```python
   from typing import Optional
   
   def process_input(user_input: str, max_length: int = 1000) -> str:
       if len(user_input) > max_length:
           raise ValueError(f"Input too long: {len(user_input)} > {max_length}")
       return user_input.strip()
   ```

3. **Dependency Security**
   - Keep dependencies updated
   - Review security advisories
   - Use `pip-audit` to check for vulnerabilities

### Documentation Standards

1. **Code Comments**
   - Explain *why*, not *what*
   - Keep comments up-to-date
   - Remove commented-out code

2. **README Updates**
   - Keep examples current
   - Update version numbers
   - Test all commands

3. **API Documentation**
   - Document all endpoints
   - Include example requests/responses
   - Note authentication requirements

## Project Structure

```
ag-ui-agent-mcp/
├── agent.py              # Main agent implementation
├── deploy.py             # Deployment utilities
├── test_client.py        # Test client
├── requirements.txt      # Python dependencies
├── Dockerfile            # Container definition
├── docker-compose.yml    # Local development
├── .env.example          # Configuration template
├── README.md            # Main documentation
├── USAGE.md             # Usage guide
└── CONTRIBUTING.md      # This file
```

## Questions?

- Open an issue for bugs or feature requests
- Tag issues appropriately
- Be respectful and constructive

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

Thank you for contributing! 🎉
