# Contributing to CalcBurst

Thank you for your interest in contributing to CalcBurst! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, AWS region)
- Relevant logs or error messages

### Suggesting Features

Feature requests are welcome! Please include:
- Clear description of the feature
- Use cases and benefits
- Potential implementation approach
- Any relevant examples

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/calcburst.git
   cd calcburst
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the coding standards below
   - Add tests for new functionality
   - Update documentation as needed

4. **Run tests**
   ```bash
   python -m pytest tests/ -v
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: your feature description"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Provide a clear description
   - Reference any related issues
   - Ensure all checks pass

## Coding Standards

### Python Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Maximum line length: 100 characters

Example:
```python
def perform_calculation(operation, operands):
    """
    Perform mathematical calculations based on operation type.
    
    Args:
        operation (str): Operation type (add, subtract, etc.)
        operands (list): List of numbers to operate on
    
    Returns:
        float: Calculation result
    
    Raises:
        ValueError: If operation is invalid or operands insufficient
    """
    # Implementation
```

### Terraform Code Style

- Use consistent indentation (2 spaces)
- Add comments for complex resources
- Use variables for configurable values
- Follow naming conventions: `resource_type-purpose`

### Commit Messages

Format: `type(scope): description`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test additions or changes
- `refactor`: Code refactoring
- `chore`: Maintenance tasks

Examples:
```
feat(lambda): add support for trigonometric operations
fix(dynamodb): resolve timeout issue on high load
docs(readme): update deployment instructions
test(calculator): add edge case tests for division
```

## Development Setup

1. **Install dependencies**
   ```bash
   pip install -r lambda/requirements.txt
   pip install pytest pylint black
   ```

2. **Set up pre-commit hooks**
   ```bash
   pip install pre-commit
   pre-commit install
   ```

3. **Configure AWS credentials**
   ```bash
   aws configure
   ```

## Testing Guidelines

### Unit Tests

- Write tests for all new functions
- Aim for >80% code coverage
- Use descriptive test names
- Test edge cases and error conditions

Example:
```python
def test_addition_with_positive_numbers(self):
    result = perform_calculation('add', [10, 20, 30])
    self.assertEqual(result, 60)

def test_division_by_zero_raises_error(self):
    with self.assertRaises(ValueError):
        perform_calculation('divide', [10, 0])
```

### Integration Tests

- Test API endpoints end-to-end
- Verify DynamoDB interactions
- Check error handling

### Load Tests

- Ensure changes don't degrade performance
- Run load tests before submitting PR
- Document performance impact

## Documentation

### Code Documentation

- Add docstrings to all public functions
- Include parameter types and return values
- Document exceptions that may be raised

### README Updates

Update README.md if you:
- Add new features
- Change API behavior
- Modify deployment process
- Update dependencies

### Architecture Documentation

Update ARCHITECTURE.md for:
- New components
- Changed data flows
- Modified infrastructure

## Review Process

1. **Automated Checks**
   - All tests must pass
   - Code coverage must not decrease
   - Linting must pass
   - Security scans must pass

2. **Code Review**
   - At least one maintainer approval required
   - Address all review comments
   - Keep discussions constructive

3. **Merge**
   - Squash commits for cleaner history
   - Delete feature branch after merge

## Release Process

1. Update version in relevant files
2. Update CHANGELOG.md
3. Create release tag
4. Deploy to production
5. Announce release

## Getting Help

- Open an issue for questions
- Join discussions in GitHub Discussions
- Check existing issues and PRs

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing to CalcBurst!

