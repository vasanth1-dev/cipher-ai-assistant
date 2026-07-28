# Clipboard Plugin

## Overview

The Clipboard plugin allows Cipher to interact with the system clipboard
through Cipher's centralized `ClipboardService`.

The plugin is intentionally lightweight and acts only as a command layer.
All clipboard implementation details remain inside the service.

---

## Features

- Copy text to clipboard
- Paste clipboard contents
- View current clipboard contents
- Clear clipboard
- View clipboard history

---

## Example Commands

### Copy

```text
copy Hello World
```

```text
copy My password hint
```

---

### Paste

```text
paste
```

---

### Show Clipboard

```text
clipboard
```

---

### Clear Clipboard

```text
clear clipboard
```

---

### Clipboard History

```text
clipboard history
```

---

## Dependencies

This plugin depends on:

- `services.clipboard_service`

---

## Required Permissions

- Clipboard

---

## Architecture

```text
User
   │
   ▼
Clipboard Plugin
   │
   ▼
ClipboardService
   │
   ▼
System Clipboard
```

The plugin never accesses the operating system clipboard directly. All
clipboard operations are delegated to `ClipboardService`, which provides
a single implementation shared across Cipher.

---

## Notes

- Clipboard history is managed by the service.
- The plugin only parses commands and formats responses.
- Future versions may support images, files, and rich text if those
  capabilities are added to `ClipboardService`.

---

## Version

- Plugin Version: **1.0.0**
- Compatible with: **Cipher v2+**