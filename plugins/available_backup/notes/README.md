# Notes Plugin

## Overview

The Notes plugin enables Cipher to create, view, open, and delete notes
through the centralized `NotesService`.

The plugin itself does not perform any file operations. It simply parses
user commands and delegates all note management to the service layer,
keeping Cipher's architecture clean and maintainable.

---

## Features

- Create notes
- View all notes
- Open a note
- Delete a note
- Uses Cipher's centralized Notes Service

---

## Example Commands

### Create Notes

```text
take note Buy groceries
```

```text
create note Meeting at 3 PM tomorrow
```

```text
add note Finish Cipher plugin framework
```

---

### View Notes

```text
show notes
```

```text
list notes
```

```text
my notes
```

---

### Open a Note

```text
open note Meeting at 3 PM tomorrow
```

---

### Delete a Note

```text
delete note Buy groceries
```

---

## Dependencies

This plugin depends on:

- `services.notes_service`

---

## Required Permissions

- Filesystem

---

## Architecture

```text
User
   │
   ▼
Notes Plugin
   │
   ▼
NotesService
   │
   ▼
Note Storage (files/database)
```

All note storage, retrieval, indexing, and persistence are handled by
`NotesService`. The plugin never accesses storage directly.

---

## Notes

- The plugin is intentionally thin and delegates all business logic.
- Future versions may support:
  - Search notes
  - Edit notes
  - Tags
  - Categories
  - Markdown notes
  - Rich text
  - Attachments
  - AI note summarization

---

## Version

- Plugin Version: **1.0.0**
- Compatible with: **Cipher v2+**