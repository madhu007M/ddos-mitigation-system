# Contributing to DDoS Mitigation System

Thank you for your interest in contributing to the DDoS Mitigation System! This document provides guidelines and instructions for contributing.

## 🤝 How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- System information (OS, Python version)
- Logs (if applicable)

### Suggesting Enhancements

We welcome feature requests! Please:
- Check if the feature already exists
- Describe the use case
- Explain why this would be useful
- Provide examples if possible

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/madhu007M/ddos-mitigation-system.git
   cd ddos-mitigation-system
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes**
   - Follow the code style
   - Add tests for new features
   - Update documentation
   - Ensure all tests pass

4. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

6. **Open a Pull Request**
   - Describe your changes
   - Reference any related issues
   - Wait for review

## 📋 Development Setup

### Prerequisites
- Python 3.8+
- pip
- git

### Setup Development Environment

```bash
# Clone the repo
git clone https://github.com/madhu007M/ddos-mitigation-system.git
cd ddos-mitigation-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m unittest discover tests
```

## 🎨 Code Style

### Python Style Guide
- Follow PEP 8
- Use type hints where applicable
- Write docstrings for classes and functions
- Keep functions focused and small

### Example

```python
def process_request(self, ip: str, endpoint: str = "/", method: str = "GET") -> tuple[bool, str, Dict]:
    """
    Process incoming request and determine if it should be allowed
    
    Args:
        ip: Client IP address
        endpoint: Request endpoint
        method: HTTP method
        
    Returns:
        Tuple of (is_allowed, reason, details)
    """
    # Implementation
    pass
```

## 🧪 Testing

### Writing Tests

- Add tests for new features
- Ensure existing tests pass
- Aim for high test coverage

```python
import unittest
from src.core.rate_limiter import RateLimiter

class TestRateLimiter(unittest.TestCase):
    def setUp(self):
        self.limiter = RateLimiter(max_requests=10, time_window=5)
    
    def test_allows_requests_under_limit(self):
        is_allowed, _ = self.limiter.is_allowed("192.168.1.1")
        self.assertTrue(is_allowed)
```

### Running Tests

```bash
# Run all tests
python -m unittest discover tests -v

# Run specific test file
python -m unittest tests.test_rate_limiter

# Run specific test
python -m unittest tests.test_rate_limiter.TestRateLimiter.test_allows_requests_under_limit
```

## 📝 Documentation

### Code Documentation
- Add docstrings to all public functions and classes
- Use clear, descriptive names
- Comment complex logic

### User Documentation
- Update README.md for user-facing changes
- Update USAGE.md for new features
- Add examples for new functionality

## 🏗️ Project Structure

```
ddos-mitigation-system/
├── src/
│   ├── core/              # Core mitigation logic
│   │   ├── config.py      # Configuration management
│   │   ├── rate_limiter.py
│   │   ├── traffic_monitor.py
│   │   ├── ip_filter.py
│   │   └── mitigation_system.py
│   └── dashboard/         # Web dashboard
│       ├── app.py
│       └── templates/
├── tests/                 # Unit and integration tests
├── logs/                  # Log files (gitignored)
├── config.yaml           # Configuration file
├── requirements.txt      # Python dependencies
├── README.md            # Main documentation
├── USAGE.md             # Usage guide
└── CONTRIBUTING.md      # This file
```

## 🔍 Code Review Process

### What We Look For
- Code quality and style
- Test coverage
- Documentation
- Performance impact
- Security considerations

### Review Timeline
- Initial review: Within 1-2 days
- Follow-up: 1 day per iteration
- Merge: After approval from maintainer

## 🐛 Bug Fix Process

1. Create an issue describing the bug
2. Reference the issue in your PR
3. Add test that reproduces the bug
4. Fix the bug
5. Verify test now passes

## ✨ Feature Development Process

1. Discuss feature in an issue first
2. Get approval from maintainers
3. Implement feature
4. Add comprehensive tests
5. Update documentation
6. Submit PR

## 📊 Performance Considerations

- Profile code for bottlenecks
- Avoid blocking operations
- Use appropriate data structures
- Consider memory usage
- Test with realistic load

## 🔒 Security Guidelines

- Never commit secrets or API keys
- Validate all user input
- Use parameterized queries
- Follow security best practices
- Report security issues privately

## 🎯 Priority Areas

We especially welcome contributions in:
- Performance optimizations
- Additional mitigation strategies
- Better visualization in dashboard
- Documentation improvements
- Test coverage
- Example integrations

## 💬 Communication

- **Issues**: For bug reports and feature requests
- **Pull Requests**: For code contributions
- **Discussions**: For questions and ideas

## ⚖️ License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be:
- Listed in README.md
- Credited in release notes
- Appreciated in the community!

## 📞 Getting Help

Stuck? Need help?
- Check existing issues
- Read the documentation
- Ask in an issue
- Be patient and respectful

## 🌟 Thank You!

Your contributions make this project better for everyone. We appreciate your time and effort!

---

**Happy Contributing!** 🚀
