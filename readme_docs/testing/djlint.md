## Django Template Linting (HTML)

Django HTML templates were tested using **djLint**, a linter designed specifically to support Django template syntax.

### Tool Used
- djLint

### Configuration
djLint was configured using `pyproject.toml` with the Django profile enabled:

```toml
[tool.djlint]
profile = "django"
indent = 2
max_line_length = 120
```

### Testing Process
The linter was run across all Django templates (run from root) using the following command:

```bash
djlint . --check
```

This process validated:
- Correct HTML structure
- Proper tag nesting and closing
- Consistent indentation
- Valid Django template syntax, including template tags and variables

### Results
All templates passed linting successfully, with no errors or required changes reported.

### Limitations
djLint validates template structure and syntax only. Runtime issues such as missing context variables or invalid URL names were tested separately using Django’s test client.
