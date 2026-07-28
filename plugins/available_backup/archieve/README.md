# Archive Plugin

The **Archive Plugin** enables Cipher v2 to create, extract, inspect, and validate archive files using Python's standard library.

---

## Features

- Create ZIP archives
- Extract ZIP archives
- Create TAR archives
- Extract TAR archives
- Support for compressed TAR formats
- List archive contents
- Validate supported archive types

---

## Supported Formats

| Format | Read | Create |
|---------|:----:|:------:|
| `.zip` | ✅ | ✅ |
| `.tar` | ✅ | ✅ |
| `.tar.gz` | ✅ | ✅ |
| `.tgz` | ✅ | ✅ |
| `.tar.bz2` | ✅ | ✅ |
| `.tbz2` | ✅ | ✅ |

---

## Planned Voice Commands

Examples:

- create zip archive
- compress this folder
- zip Downloads
- extract archive
- unzip file
- extract to Desktop
- show archive contents

> At present, the plugin exposes archive functionality and is intended to be invoked by Cipher's structured file-intent pipeline.

---

## Public Methods

### ZIP

- `create_zip()`
- `extract_zip()`
- `list_zip()`

### TAR

- `create_tar()`
- `extract_tar()`
- `list_tar()`

### Validation

- `is_supported()`
- `exists()`

---

## Example

Create a ZIP archive:

```python
plugin.create_zip(
    Path("/home/user/Documents"),
    Path("/home/user/Documents.zip")
)
```

Extract a ZIP archive:

```python
plugin.extract_zip(
    Path("Documents.zip"),
    Path("/home/user/Desktop")
)
```

List contents:

```python
files = plugin.list_zip(
    Path("Documents.zip")
)
```

---

## Dependencies

Uses only the Python standard library:

- `zipfile`
- `tarfile`
- `pathlib`

No external packages are required.

---

## Security Notes

- Archive extraction destinations should be validated by higher-level components before extraction.
- Future versions will include protection against directory traversal ("Zip Slip") attacks by validating extracted paths.

---

## Future Enhancements

Planned capabilities include:

- Password-protected ZIP archives
- 7z archive support
- RAR archive support (read support where available)
- Archive encryption
- Progress reporting
- Drag-and-drop GUI integration
- Recursive archive inspection
- Duplicate file detection
- Integrity verification
- Batch archive operations

---

Part of the **Cipher v2 Professional Ubuntu AI Assistant** plugin ecosystem.