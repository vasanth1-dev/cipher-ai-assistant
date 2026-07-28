# Text Tools Plugin

The **Text Tools Plugin** provides reusable text-processing utilities for Cipher v2. It serves both the assistant and other plugins that need text transformation or analysis.

---

## Features

- Convert text to uppercase
- Convert text to lowercase
- Convert text to title case
- Convert text to sentence case
- Count words
- Count characters
- Count lines
- Remove extra whitespace
- Reverse text
- Generate URL-friendly slugs

---

## Planned Voice Commands

Examples:

- convert this to uppercase
- make this lowercase
- title case this sentence
- sentence case
- reverse this text
- count the words
- count the characters
- clean this text
- generate a slug

These commands will be handled through Cipher's structured text-intent pipeline.

---

## Public Methods

### Case Conversion

```python
uppercase(text)
lowercase(text)
titlecase(text)
sentencecase(text)
```

---

### Statistics

```python
word_count(text)
character_count(text)
line_count(text)
```

---

### Formatting

```python
clean_whitespace(text)
reverse(text)
slug(text)
```

---

## Example Usage

Convert to uppercase:

```python
plugin.uppercase("hello world")
```

Output:

```text
HELLO WORLD
```

Generate a slug:

```python
plugin.slug("Cipher v2 Professional Assistant")
```

Output:

```text
cipher-v2-professional-assistant
```

---

## Dependencies

Uses only the Python standard library.

No external packages are required.

---

## Future Enhancements

Planned capabilities include:

- Markdown formatting
- HTML to plain text conversion
- Unicode normalization
- Duplicate line removal
- Sort and deduplicate lines
- Base64 encoding/decoding
- Hash generation (SHA-256, MD5)
- Regex utilities
- Text diff generation
- AI-powered grammar improvement
- Automatic language detection

---

Part of the **Cipher v2 Professional Ubuntu AI Assistant** plugin ecosystem.