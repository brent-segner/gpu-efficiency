# Contributing to GPU Efficiency Analytics

Thank you for your interest in contributing to this project! This guide will help you get started.

## 🎯 Ways to Contribute

We welcome contributions in several areas:

### 1. Code Contributions
- **New workload scenarios** for synthetic data generation
- **Additional visualizations** and analysis techniques
- **Performance optimizations** for large datasets
- **Integration examples** with monitoring platforms (Grafana, DataDog, New Relic)
- **Real DCGM data parsers** and utilities

### 2. Documentation
- **Tutorial notebooks** for specific use cases
- **Cloud provider guides** (AWS, GCP, Azure)
- **Best practices** documentation
- **Translation** of documentation to other languages

### 3. Testing
- **Test cases** for data validation
- **Edge case handling**
- **Performance benchmarks**

### 4. Bug Reports
- Report issues with clear reproduction steps
- Include environment details (Python version, OS, etc.)
- Provide sample data if possible

## 🚀 Getting Started

### Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/yourusername/gpu-efficiency-analytics.git
cd gpu-efficiency-analytics

# Add upstream remote
git remote add upstream https://github.com/originalauthor/gpu-efficiency-analytics.git
```

### Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 jupyter
```

### Run Tests

```bash
# Generate synthetic data
python generate_synthetic_data.py

# Run quick analysis
python quick_start.py

# Launch Jupyter notebook
jupyter notebook gpu_efficiency_analysis.ipynb
```

## 📝 Contribution Guidelines

### Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and under 50 lines when possible

Example:
```python
def calculate_efficiency_metrics(df):
    """
    Calculate GPU efficiency metrics including PIF, Realized TFLOPS, and RFU.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing DCGM metrics
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with additional efficiency metric columns
    """
    # Implementation here
    pass
```

### Commit Messages

Use clear, descriptive commit messages:

```
Good: "Add support for NVIDIA L40 GPU specifications"
Bad: "Updated file"

Good: "Fix power calculation for edge case when GPU is idle"
Bad: "Bug fix"
```

Format:
```
[Type] Brief description (50 chars or less)

Longer explanation if needed (wrap at 72 chars)

- Bullet points for details
- Reference issues: Fixes #123
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write code
   - Add tests if applicable
   - Update documentation

3. **Test thoroughly**
   ```bash
   python quick_start.py
   # Test any new features
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: Add XYZ feature"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request**
   - Go to GitHub and create a PR
   - Fill out the PR template
   - Link any related issues
   - Request review

### Pull Request Template

When creating a PR, include:

```markdown
## Description
Brief description of changes

## Motivation and Context
Why is this change needed?

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
Describe testing performed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Documentation has been updated
- [ ] Tests pass locally
- [ ] Comments added for complex logic
```

## 🐛 Reporting Bugs

When reporting bugs, include:

1. **Environment details**
   - Python version
   - Operating system
   - Package versions (`pip freeze`)

2. **Steps to reproduce**
   - Exact commands run
   - Sample data if relevant
   - Expected vs actual behavior

3. **Error messages**
   - Full stack trace
   - Relevant log output

Example bug report:
```markdown
**Environment:**
- Python 3.9.5
- Ubuntu 20.04
- pandas 1.3.0

**Steps to Reproduce:**
1. Run `python generate_synthetic_data.py`
2. Run `python quick_start.py`
3. See error

**Expected Behavior:**
Script should complete successfully

**Actual Behavior:**
KeyError on line 45

**Stack Trace:**
[paste full error]
```

## 💡 Feature Requests

Feature requests are welcome! Please:

1. Check if the feature already exists or is planned
2. Describe the use case clearly
3. Explain the expected behavior
4. Provide examples if applicable

## 📚 Areas Needing Help

Current priorities:

### High Priority
- [ ] Integration with Prometheus/Grafana
- [ ] Support for AMD GPUs (MI250X, MI300)
- [ ] Real-time streaming analysis examples
- [ ] Cost modeling and TCO calculator

### Medium Priority
- [ ] Additional visualization types (heatmaps, sankey diagrams)
- [ ] Export to PowerBI/Tableau
- [ ] Multi-cluster comparison tools
- [ ] Historical trend analysis

### Nice to Have
- [ ] Web dashboard (Flask/Streamlit)
- [ ] Automated alerting examples
- [ ] Machine learning for anomaly detection
- [ ] Integration with SLURM/Kubernetes

## 🤝 Code Review Process

All contributions go through code review:

1. Maintainer reviews the PR
2. Feedback provided as comments
3. Address feedback and update PR
4. Approval and merge

Review criteria:
- Code quality and style
- Documentation completeness
- Test coverage
- Performance impact
- Breaking changes (avoided when possible)

## 📧 Questions?

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and community discussion
- **Email**: [maintainer email] for private matters

## 🙏 Recognition

Contributors will be:
- Listed in README.md
- Credited in release notes
- Thanked in commit messages

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for making GPU efficiency analytics better for everyone! 🚀
