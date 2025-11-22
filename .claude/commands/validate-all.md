# Validate All Assets and Code

Run comprehensive validation on the entire project:

1. Run enhanced asset validator
2. Run scene limits validation
3. Run background tiles validation
4. Run JSON schema validation
5. Run linting (ruff)
6. Run type checking (mypy)
7. Run test suite

Execute the following commands:

```bash
# Enhanced asset validation with suggestions
python scripts/validation/enhanced_validator.py

# GB Studio validations
python scripts/validation/check_scene_limits.py
python scripts/validation/check_bg_tiles.py
python scripts/validation/check_json_schema.py

# Code quality checks
ruff check .
mypy .

# Test suite
pytest --cov=.langflow --cov-report=term-missing
```

After completion, provide a summary of:
- Total issues found
- Warnings that need attention
- Suggestions for improvement
- Test coverage percentage
- Overall project health status
