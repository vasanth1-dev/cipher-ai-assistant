# Clipboard History Plugin

The **Clipboard History Plugin** provides clipboard history management for Cipher v2. It is designed to work with a background clipboard monitoring service that records copied text and makes it available to the assistant and GUI.

---

## Features

- Store clipboard history in memory
- Prevent consecutive duplicate entries
- Retrieve recent clipboard items
- Search clipboard history
- Clear clipboard history
- Configurable history size
- Snapshot of clipboard state

---

## Architecture

This plugin **does not monitor the system clipboard directly**.

Instead:

```
System Clipboard
        │
        ▼
Clipboard Monitor Service
        │
        ▼
ClipboardHistoryPlugin
        │
        ▼
Cipher Assistant / GUI
```

This separation keeps the plugin lightweight and reusable.

---

## Planned Voice Commands

Examples:

- show clipboard history
- what did I copy last
- clipboard manager
- search clipboard for password
- clear clipboard history
- show recent copied text

These commands will be connected through Cipher's structured clipboard-intent pipeline.

---

## Public Methods

### Add Item

```python
add(text)
```

Stores a new clipboard entry.

---

### Recent Items

```python
recent(limit=10)
```

Returns the newest clipboard entries.

---

### Search

```python
search("invoice")
```

Returns matching clipboard entries.

---

### Clear

```python
clear()
```

Removes all stored clipboard items.

---

### Count

```python
count()
```

Returns the number of stored entries.

---

### Capacity

```python
set_limit(250)
```

Updates the maximum history size.

---

### Snapshot

```python
snapshot()
```

Returns:

```python
{
    "count": 18,
    "capacity": 100,
    "items": [...]
}
```

---

## Storage

The current implementation keeps clipboard history **in memory only**.

Future versions may support encrypted persistent storage.

---

## Dependencies

Uses only the Python standard library.

No external packages are required.

---

## Future Enhancements

Planned capabilities include:

- Persistent encrypted history
- Clipboard images
- Rich text support
- File copy history
- Favorite clipboard entries
- Clipboard synchronization across devices
- Automatic expiration rules
- Duplicate detection beyond consecutive entries
- Clipboard categories
- AI-powered clipboard search and summarization

---

Part of the **Cipher v2 Professional Ubuntu AI Assistant** plugin ecosystem.