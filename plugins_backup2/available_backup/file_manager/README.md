# File Manager Plugin

## Overview

The File Manager plugin enables Cipher to perform common file and folder
operations through the centralized `FileManagerService`.

The plugin itself contains no filesystem logic. It only:

- Detects supported file management commands
- Delegates requests to `FileManagerService`
- Returns formatted responses to the user

This separation keeps Cipher's architecture clean and makes the
filesystem implementation reusable throughout the application.

---

## Features

- Create folders
- Create files
- Delete files
- Delete folders
- Rename files
- Rename folders
- Move files
- Copy files
- List files
- List folders
- Open files
- Open folders

---

## Example Commands

### Create

```text
create folder Projects
```

```text
mkdir Cipher
```

```text
create file notes.txt
```

---

### Delete

```text
delete file notes.txt
```

```text
delete folder OldProjects
```

---

### Rename

```text
rename file old.txt to new.txt
```

```text
rename folder Work to Office
```

---

### Move / Copy

```text
move file report.pdf to Documents
```

```text
copy file image.png to Pictures
```

---

### List

```text
list files
```

```text
list folders
```

---

### Open

```text
open file notes.txt
```

```text
open folder Downloads
```

---

## Dependencies

This plugin depends on:

- `services.file_manager_service`

---

## Required Permissions

- Filesystem

---

## Architecture

```text
User
   │
   ▼
FileManager Plugin
   │
   ▼
FileManagerService
   │
   ▼
Operating System Filesystem
```

The plugin never performs filesystem operations directly. All path
validation, permissions, file manipulation, and platform-specific logic
should remain inside `FileManagerService`.

---

## Future Enhancements

Potential future capabilities include:

- Search files
- Bulk operations
- Undo delete
- Compress / Extract archives
- File properties
- Favorites
- Recent files
- Duplicate finder
- Secure delete
- AI-powered file organization

---

## Version

- Plugin Version: **1.0.0**
- Compatible with: **Cipher v2+**