# Hash Tools Plugin

The **Hash Tools Plugin** provides cryptographic hash generation and verification utilities for Cipher v2. It supports hashing both text and files using Python's standard `hashlib` module.

---

## Features

- Generate hashes from text
- Generate hashes from files
- Verify file integrity using checksums
- Multiple hashing algorithms
- Streaming file hashing for large files
- No external Python dependencies

---

## Supported Algorithms

Commonly available algorithms include:

- MD5
- SHA1
- SHA224
- SHA256
- SHA384
- SHA512
- SHA3 family (platform dependent)
- BLAKE2 family (platform dependent)

The complete list can be obtained programmatically:

```python
plugin.algorithms()
```

---

## Planned Voice Commands

Examples:

- generate sha256 hash
- create md5 checksum
- hash this file
- verify checksum
- compare sha512 hash
- calculate file hash

These commands will be processed by Cipher's structured security-intent pipeline.

---

## Public Methods

### Hash Text

```python
hash_text(
    text,
    algorithm="sha256"
)
```

---

### Hash File

```python
hash_file(
    Path("example.iso"),
    algorithm="sha256"
)
```

---

### Verify File

```python
verify_file(
    Path("example.iso"),
    expected_hash,
    algorithm="sha256"
)
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

### Supported Algorithms

```python
algorithms()
```

Returns all algorithms supported by the local Python installation.

---

## Dependencies

Uses only the Python standard library:

- `hashlib`
- `pathlib`

No external packages are required.

---

## Performance

- Files are processed in **1 MB chunks** to support hashing very large files efficiently without loading the entire file into memory.

---

## Error Handling

The plugin reports errors when:

- the file does not exist
- the requested hash algorithm is unsupported
- the file cannot be read

Errors are also recorded through Cipher's logging system.

---

## Future Enhancements

Planned capabilities include:

- Directory hashing
- Recursive checksum generation
- Manifest file creation
- Checksum export/import
- Digital signature verification
- HMAC generation
- Password-based key derivation helpers
- GUI checksum comparison
- Batch file verification
- Integration with Cipher's download manager

---

Part of the **Cipher v2 Professional Ubuntu AI Assistant** plugin ecosystem.