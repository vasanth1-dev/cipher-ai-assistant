# Code Tools Plugin

The **Code Tools Plugin** provides lightweight source code utilities for Cipher v2. It is intended for developer workflows, IDE integration, and future AI-assisted programming features.

---

## Features

- Detect programming language from file extension
- Basic source code statistics
- Python syntax validation
- Remove Python single-line comments
- Reusable API for developer tools

---

## Planned Voice Commands

Examples:

- analyze this code
- validate Python code
- detect programming language
- show code statistics
- remove comments
- inspect source file

These requests will be routed through Cipher's structured developer-intent pipeline.

---

## Public Methods

### Detect Language

```python
detect_language(path)
```

Example:

```python
plugin.detect_language(
    Path("main.py")
)
```

Returns:

```text
Python
```

---

### Code Statistics

```python
statistics(code)
```

Returns:

```python
{
    "lines": 182,
    "blank_lines": 28,
    "comment_lines": 17,
    "characters": 5482
}
```

---

### Validate Python

```python
validate_python(code)
```

Returns:

```python
(True, "Valid Python")
```

or

```python
(False, "<syntax error>")
```

---

### Remove Comments

```python
remove_python_comments(code)
```

Removes Python single-line (`#`) comments while preserving the remaining code.

---

## Dependencies

Uses only the Python standard library:

- `ast`
- `re`
- `pathlib`

No external packages are required.

---

## Error Handling

The plugin reports errors when:

- invalid Python syntax is encountered
- unsupported languages are requested for language-specific operations

Exceptions are also recorded through Cipher's logging system.

---

## Future Enhancements

Planned capabilities include:

- Multi-language syntax validation
- Automatic formatting (Black, Prettier, etc.)
- Code complexity metrics
- Function/class extraction
- TODO/FIXME detection
- Duplicate code detection
- Static analysis integration
- Git integration
- AI-powered code review
- AI-generated documentation
- Security vulnerability scanning

---

Part of the **Cipher v2 Professional Ubuntu AI Assistant** plugin ecosystem.