# JSON Tools Plugin

The **JSON Tools Plugin** provides utilities for validating, formatting, normalizing, and minifying JSON documents. It is intended for use by Cipher's assistant, developer tools, and other plugins.

---

## Features

- Validate JSON syntax
- Pretty-print JSON
- Minify JSON
- Normalize JSON
- Sort object keys
- Unicode-safe output

---

## Planned Voice Commands

Examples:

- validate this JSON
- format this JSON
- pretty print JSON
- minify JSON
- normalize JSON
- sort JSON keys

These requests will be routed through Cipher's structured developer-intent pipeline.

---

## Public Methods

### Validate

```python
validate(text)
```

Returns:

```python
(True, "Valid JSON")
```

or

```python
(False, "<error message>")
```

---

### Pretty Print

```python
pretty(
    text,
    indent=4,
    sort_keys=False
)
```

---

### Minify

```python
minify(text)
```

---

### Normalize

Produces deterministic JSON output with sorted keys and minimal whitespace.

```python
normalize(text)
```

---

## Example Usage

Pretty-print:

```python
formatted = plugin.pretty(json_text)
```

Minify:

```python
compressed = plugin.minify(json_text)
```

Normalize:

```python
normalized = plugin.normalize(json_text)
```

---

## Dependencies

Uses only the Python standard library:

- `json`

No external packages are required.

---

## Error Handling

The plugin reports JSON parsing errors when:

- invalid syntax is detected
- malformed JSON is supplied

Exceptions are also logged through Cipher's logging system.

---

## Future Enhancements

Planned capabilities include:

- JSON schema validation
- JSONPath queries
- JSON diff and merge
- YAML ↔ JSON conversion
- TOML ↔ JSON conversion
- XML ↔ JSON conversion
- Large file streaming support
- JSON repair suggestions
- Syntax highlighting
- AI-assisted JSON explanation

---

Part of the **Cipher v2 Professional Ubuntu AI Assistant** plugin ecosystem.