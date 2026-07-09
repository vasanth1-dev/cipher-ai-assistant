# Markdown Tools Plugin

The **Markdown Tools Plugin** provides Markdown processing utilities for Cipher v2. It supports document conversion, validation, statistics, and structure analysis for developer workflows.

---

## Features

- Validate Markdown documents
- Convert Markdown to HTML
- Convert HTML to Markdown
- Generate a table of contents (TOC)
- Document statistics
- Heading analysis

---

## Planned Voice Commands

Examples:

- convert markdown to HTML
- convert HTML to markdown
- validate markdown
- generate table of contents
- analyze markdown document
- markdown statistics

These requests will be routed through Cipher's structured document and developer-intent pipeline.

---

## Public Methods

### Validate

```python
validate(text)
```

Returns:

```python
(True, "Valid Markdown")
```

---

### Markdown → HTML

```python
markdown_to_html(text)
```

---

### HTML → Markdown

```python
html_to_markdown(text)
```

---

### Table of Contents

```python
table_of_contents(text)
```

Example output:

```python
[
    {
        "level": 1,
        "title": "Introduction"
    },
    {
        "level": 2,
        "title": "Installation"
    }
]
```

---

### Statistics

```python
statistics(text)
```

Returns:

```python
{
    "lines": 128,
    "words": 846,
    "characters": 5120,
    "headings": 12,
    "links": 18,
    "images": 4
}
```

---

## Dependencies

Python packages:

- `markdown`
- `markdownify`

Install:

```bash
pip install markdown markdownify
```

---

## Error Handling

The plugin reports errors when:

- required conversion libraries are unavailable
- invalid input is supplied

Exceptions are also written to Cipher's logging system.

---

## Future Enhancements

Planned capabilities include:

- Markdown linting
- GitHub Flavored Markdown support
- Mermaid diagram detection
- Markdown ↔ PDF conversion
- Markdown ↔ DOCX conversion
- Front matter parsing
- Link validation
- Automatic TOC insertion
- AI-powered document summarization
- AI-assisted Markdown editing

---

Part of the **Cipher v2 Professional Ubuntu AI Assistant** plugin ecosystem.