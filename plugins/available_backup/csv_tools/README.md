# CSV Tools Plugin

The **CSV Tools Plugin** provides utilities for reading, writing, validating, and inspecting CSV files. It is designed for use by Cipher's assistant, data-analysis features, and developer tools.

---

## Features

- Read CSV files into dictionaries
- Write CSV files from dictionaries
- Validate CSV files
- Retrieve column headers
- Inspect CSV metadata
- UTF-8 support

---

## Planned Voice Commands

Examples:

- read this CSV
- validate CSV file
- show CSV columns
- how many rows are in this CSV
- export data to CSV
- open CSV file

These requests will be routed through Cipher's structured document and developer intent pipeline.

---

## Public Methods

### Read

```python
read(path)
```

Returns:

```python
[
    {
        "Name": "Alice",
        "Age": "25"
    },
    {
        "Name": "Bob",
        "Age": "31"
    }
]
```

---

### Headers

```python
headers(path)
```

Returns:

```python
[
    "Name",
    "Age"
]
```

---

### Write

```python
write(
    path,
    rows
)
```

Creates a CSV file from a list of dictionaries.

---

### Validate

```python
validate(path)
```

Returns:

```python
(True, "Valid CSV")
```

or

```python
(False, "<error message>")
```

---

### Metadata

```python
info(path)
```

Returns:

```python
{
    "rows": 250,
    "columns": 8,
    "headers": [
        "Name",
        "Email",
        "Department"
    ]
}
```

---

## Dependencies

Uses only the Python standard library:

- `csv`
- `pathlib`

No external packages are required.

---

## Error Handling

The plugin reports errors when:

- the file cannot be opened
- invalid CSV data is encountered
- no rows are supplied during writing

Exceptions are also written to Cipher's logging system.

---

## Future Enhancements

Planned capabilities include:

- CSV filtering
- CSV sorting
- CSV merging
- Duplicate row detection
- Large-file streaming
- CSV ↔ Excel conversion
- CSV ↔ JSON conversion
- Automatic delimiter detection
- Type inference
- AI-assisted data profiling

---

Part of the **Cipher v2 Professional Ubuntu AI Assistant** plugin ecosystem.