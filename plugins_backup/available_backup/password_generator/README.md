# Password Generator Plugin

The **Password Generator Plugin** generates cryptographically secure passwords for Cipher v2 and provides a basic password strength evaluation utility.

---

## Features

- Cryptographically secure password generation
- Configurable password length
- Uppercase letters
- Lowercase letters
- Numbers
- Symbols
- Password strength evaluation
- Reusable API for other Cipher components

---

## Planned Voice Commands

Examples:

- generate a password
- create a strong password
- generate a 20 character password
- create a password with symbols
- check password strength

These commands will be handled through Cipher's structured security-intent pipeline.

---

## Public Methods

### Generate Password

```python
generate(
    length=16,
    uppercase=True,
    lowercase=True,
    digits=True,
    symbols=True
)
```

Example:

```python
password = plugin.generate(
    length=20
)
```

Possible output:

```text
K!9wQ@4hLm2#ZvX8Pd$r
```

---

### Password Strength

```python
strength(password)
```

Example output:

```python
{
    "score": 6,
    "max_score": 6,
    "rating": "Excellent",
    "length": 20
}
```

---

## Security

The plugin uses Python's `secrets` module, which is designed for generating cryptographically secure random values suitable for passwords and security tokens.

Each enabled character group contributes at least one character to the generated password.

---

## Dependencies

Uses only the Python standard library:

- `secrets`
- `string`

No external packages are required.

---

## Error Handling

The plugin reports errors when:

- no character groups are enabled
- invalid generation parameters are supplied

Errors are also written to Cipher's logging system.

---

## Future Enhancements

Planned capabilities include:

- Passphrase generation (Diceware style)
- Password policy profiles
- Custom symbol sets
- Pronounceable passwords
- Password entropy calculation
- Breach database checking
- Password history generation
- Secure password export
- Password manager integration
- AI-assisted password policy recommendations

---

Part of the **Cipher v2 Professional Ubuntu AI Assistant** plugin ecosystem.