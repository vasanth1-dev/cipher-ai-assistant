# Application Launcher Plugin

## Overview

The Application Launcher plugin enables Cipher to launch, close, and
manage desktop applications through the centralized
`AppLauncherService`.

The plugin itself never starts or terminates processes directly. Its
responsibilities are limited to:

- Detecting application-related commands
- Extracting the application name
- Delegating requests to `AppLauncherService`
- Returning formatted responses

This design keeps all operating system and process management logic
inside the service layer.

---

## Features

- Launch desktop applications
- Open applications by name
- Close running applications
- Quit applications
- Force terminate applications
- Natural language application commands

---

## Example Commands

### Launch Applications

```text
open application Firefox
```

```text
open app VS Code
```

```text
launch Terminal
```

```text
start Calculator
```

```text
run Spotify
```

---

### Close Applications

```text
close Firefox
```

```text
quit VLC
```

```text
kill Chrome
```

---

## Dependencies

This plugin depends on:

- `services.app_launcher_service`

---

## Required Permissions

- System
- Process

---

## Architecture

```text
User
   │
   ▼
Application Launcher Plugin
   │
   ▼
AppLauncherService
   │
   ▼
Operating System Process Manager
```

The plugin never executes system commands directly. All application
discovery, launching, process lookup, termination, and platform-specific
logic should remain inside `AppLauncherService`.

---

## Future Enhancements

Potential future capabilities include:

- List installed applications
- List running applications
- Recent applications
- Favorite applications
- Application aliases
- Open with specific arguments
- Workspace/session restoration
- Cross-platform application mapping
- AI-based application suggestions

---

## Version

- Plugin Version: **1.0.0**
- Compatible with: **Cipher v2+**
