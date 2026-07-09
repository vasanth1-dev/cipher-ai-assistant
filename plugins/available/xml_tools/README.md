# XML Tools Plugin

The **XML Tools Plugin** provides utilities for parsing, validating, formatting, and inspecting XML documents. It is designed for Cipher's developer features, document processing, and integration workflows.

---

## Features

- Validate XML syntax
- Parse XML documents
- Pretty-print XML
- Convert XML to Python dictionaries
- Read XML attributes
- UTF-8 compatible processing

---

## Planned Voice Commands

Examples:

- validate this XML
- pretty print XML
- format XML
- parse XML
- convert XML to dictionary
- inspect XML document

These requests will be routed through Cipher's structured developer-intent pipeline.

---

## Public Methods

### Validate

```python
validate(text)
```

Returns:

```python
(True, "Valid XML")
```

or

```python
(False, "<parse error>")
```

---

### Parse

```python
parse(text)
```

Returns the XML root element.

---

### Convert to Dictionary

```python
to_dict(text)
```

Example:

XML:

```xml
<user id="1">
    <name>Vasanth</name>
    <role>Developer</role>
</user>
```

Result:

```python
{
    "name": "Vasanth",
    "role": "Developer",
    "@attributes": {
        "id": "1"
    }
}
```

---

### Pretty Print

```python
pretty(text)
```

Produces indented, human-readable XML.

---

## Dependencies

Uses only the Python standard library:

- `xml.etree.ElementTree`
- `xml.dom.minidom`

No external packages are required.

---

## Error Handling

The plugin reports parsing errors when:

- malformed XML is supplied
- invalid XML syntax is encountered

Exceptions are also recorded through Cipher's logging system.

---

## Future Enhancements

Planned capabilities include:

- XML Schema (XSD) validation
- XPath support
- XML ↔ JSON conversion
- XML diff and merge
- Namespace utilities
- Streaming parser for large XML files
- XML compression
- XML signing and verification
- AI-assisted XML explanation
- SOAP message utilities

---

Part of the **Cipher v2 Professional Ubuntu AI Assistant** plugin ecosystem.