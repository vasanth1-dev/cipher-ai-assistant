# Document Tools Plugin

The **Document Tools Plugin** provides lightweight document processing utilities for Cipher v2. It is intended for use by the assistant, document workflows, and other plugins that work with text-based files.

---

## Features

- Read text documents
- Write text documents
- Detect supported document types
- Generate document statistics
- Search text within documents
- UTF-8 support

---

## Supported File Types

| Extension | Supported |
|-----------|:---------:|
| `.txt` | ✅ |
| `.md` | ✅ |
| `.log` | ✅ |
| `.csv` | ✅ |
| `.json` | ✅ |
| `.xml` | ✅ |
| `.yaml` | ✅ |
| `.yml` | ✅ |

---

## Planned Voice Commands

Examples:

- open this document
- read this text file
- search this document
- write to a document
- count words in this file
- document statistics

These requests will be routed through Cipher's structured document-intent pipeline.

---

## Public Methods

### Read

```python
read(path)
```

Reads a UTF-8 text document and returns its contents.

---

### Write

```python
write(
    path,
    text
)
```

Creates parent directories automatically when needed.

---

### Statistics

```python
statistics(text)
```

Returns:

```python
{
    "lines": 248,
    "words": 3814,
    "characters": 25102,
    "non_empty_lines": 231
}
```

---

### Search

```python
search(
    text,
    "cipher"
)
```

Returns a list of matching line numbers:

```python
[
    8,
    25,
    112
]
```

---

### File Type Check

```python
is_supported(path)
```

Returns:

```python
True
```

or

```python
False
```

---

## Dependencies

Uses only the Python standard library:

- `pathlib`

No external packages are required.

---

## Error Handling

The plugin reports errors when:

- the file cannot be opened
- invalid encoding is encountered
- the destination cannot be written

Exceptions are also logged through Cipher's logging system.

---

## Future Enhancements

Planned capabilities include:

- DOCX support
- ODT support
- Rich-text processing
- Encoding detection
- Large-file streaming
- Document comparison
- Automatic backups
- AI-powered summarization
- AI-powered proofreading
- Semantic document search

---

Part of the **Cipher v2 Professional Ubuntu AI Assistant** plugin ecosystem.