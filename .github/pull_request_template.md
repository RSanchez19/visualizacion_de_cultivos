# Pull Request

## 📋 Description
<!-- Brief description of what this PR does -->

## 🔍 Type of Change
<!-- Mark with an `x` all the checkboxes that apply -->
- [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
- [ ] ✨ New feature (non-breaking change which adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📚 Documentation update
- [ ] 🧪 Test coverage improvement
- [ ] 🔧 Code refactoring
- [ ] ⚡ Performance improvement

## 🧪 Testing
<!-- Describe the tests that you ran to verify your changes -->
- [ ] I have run the unit tests locally (`make test` or `python run_tests.py`)
- [ ] I have run the functional tests locally
- [ ] I have verified that coverage is at least 60%
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes

## 📊 Coverage Report
<!-- Include coverage information if you've made significant changes -->
```bash
# Run this command and paste the output:
# python run_tests.py --type unit
```

## 📋 Checklist
<!-- Mark with an `x` all the checkboxes that apply -->

### Code Quality
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings or errors

### Testing Requirements
- [ ] I have added unit tests for new functionality
- [ ] I have added functional tests where appropriate
- [ ] Test coverage is maintained at 60% or higher
- [ ] All existing tests still pass

### CI/CD Requirements
- [ ] My code passes all CI/CD quality checks
- [ ] I have tested my changes locally before pushing
- [ ] I have resolved any linting issues
- [ ] I have resolved any security issues identified by Bandit

### QGIS Plugin Specific
- [ ] I have tested the plugin in QGIS (if applicable)
- [ ] I have verified that the plugin loads correctly
- [ ] I have tested the UI components (if applicable)
- [ ] I have verified that the plugin works with the target QGIS version

## 📸 Screenshots
<!-- If applicable, add screenshots to help explain your changes -->

## 🔗 Related Issues
<!-- Link to any related issues -->
Closes #
Related to #

## 🚀 Deployment Notes
<!-- Any special notes for deployment -->
- [ ] This change requires a migration
- [ ] This change requires documentation updates
- [ ] This change requires environment variables updates
- [ ] This change is backward compatible

## 📝 Additional Notes
<!-- Any additional information that reviewers should know -->

---

## 🤖 Automated Checks
<!-- The following will be automatically checked by CI/CD -->
- [ ] ✅ Code formatting (Black)
- [ ] ✅ Import sorting (isort)
- [ ] ✅ Linting (Flake8)
- [ ] ✅ Security scan (Bandit)
- [ ] ✅ Unit tests pass
- [ ] ✅ Functional tests pass
- [ ] ✅ Coverage ≥ 60%
- [ ] ✅ Documentation builds

<!-- 
Note: All automated checks must pass before this PR can be merged.
If any checks fail, please review the CI/CD output and fix the issues.
--> 