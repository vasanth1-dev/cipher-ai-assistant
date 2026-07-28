# Settings Plugin

## Overview

The Settings plugin provides a unified interface for viewing and managing
Cipher's configuration through the centralized `SettingsService`.

The plugin itself does not read or write configuration files directly.
Its responsibilities are limited to:

- Detecting settings-related commands
- Parsing user requests
- Delegating operations to `SettingsService`
- Returning formatted responses

This architecture keeps configuration management centralized, making it
easier to maintain and extend.

---

## Features

- View current settings
- Open the settings interface
- Reload configuration
- Reset settings
- Change configuration values
- Natural language settings commands

---

## Example Commands

### View Settings

```text
settings
```

```text
show settings
```

---

### Open Settings

```text
open settings
```

---

### Reload Configuration

```text
reload settings
```

---

### Reset Configuration

```text
reset settings
```

---

### Modify Settings

```text
set speech_rate = 170
```

```text
set wake_word = hey cipher
```

```text
change theme to dark
```

```text
change model to phi3
```

---

## Dependencies

This plugin depends on:

- `services.settings_service`

---

## Required Permissions

- Settings

---

## Architecture

```text
User
   │
   ▼
Settings Plugin
   │
   ▼
SettingsService
   │
   ▼
Cipher Configuration
(config.py / settings.json / future GUI settings)
```

The plugin never edits configuration files directly. All validation,
saving, loading, migration, and defaults should remain inside
`SettingsService`.

---

## Future Enhancements

Potential future capabilities include:

- GUI settings page integration
- Import/export settings
- Multiple user profiles
- Theme management
- Voice profile selection
- Hotkey configuration
- Plugin enable/disable management
- Backup and restore configuration
- Settings synchronization

---

## Version

- Plugin Version: **1.0.0**
- Compatible with: **Cipher v2+**