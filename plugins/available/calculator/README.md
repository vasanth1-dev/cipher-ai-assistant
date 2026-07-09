# Calculator Plugin

## Overview

The Calculator plugin provides safe arithmetic evaluation for Cipher.

Unlike Python's built-in `eval()`, this plugin parses expressions using
the Abstract Syntax Tree (AST) and only allows approved mathematical
operations.

## Supported Operations

- Addition (`+`)
- Subtraction (`-`)
- Multiplication (`*`)
- Division (`/`)
- Floor Division (`//`)
- Modulus (`%`)
- Power (`**`)
- Parentheses (`()`)

## Example Commands

```
calculate 25 + 10
```

```
calc 15 * 8
```

```
math (25 + 5) / 6
```

## Example Output

```
35
```

```
120
```

```
5
```

## Safety

The plugin does **not** execute arbitrary Python code.

Unsupported expressions include:

- Variables
- Function calls
- Attribute access
- Imports
- Lists
- Dictionaries
- Loops
- Comprehensions

Only numeric arithmetic expressions are accepted.

## Version

- Plugin: 1.0.0
- Compatible with: Cipher v2+