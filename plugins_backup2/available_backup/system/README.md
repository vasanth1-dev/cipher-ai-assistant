# System Plugin

## Overview

The System plugin allows Cipher to perform operating system actions by
delegating all platform-specific functionality to Cipher's
`SystemService`.

The plugin itself contains **no operating system implementation**. Its
responsibility is limited to:

- Detecting supported system commands
- Validating the request
- Forwarding the request to `SystemService`
- Returning the service response

This keeps the plugin lightweight while ensuring that all operating
system logic remains centralized.

---

## Features

- Shutdown computer
- Restart / Reboot
- Lock screen
- Logout / Sign out
- Sleep
- Hibernate
- Mute / Unmute audio
- Volume control
- Brightness control
- Screenshot capture

---

## Example Commands

### Power

```text
shutdown
```

```text
restart
```

```text
reboot
```

```text
sleep
```

```text
hibernate
```

---

### Session

```text
lock screen
```

```text
logout
```

```text
sign out
```

---

### Audio

```text
mute
```

```text
unmute
```

```text
volume 50
```

```text
volume 80
```

---

### Display

```text
brightness 40
```

```text
brightness 100
```

---

### Screenshot

```text
take screenshot
```

```text
screenshot
```

---

## Dependencies

This plugin depends on:

- `services.system_service`

---

## Required Permissions

- System
- Shell
- Audio

---

## Architecture

```
User
   │
   ▼
System Plugin
   │
   ▼
SystemService
   │
   ▼
Ubuntu / Linux
```

The plugin never executes shell commands directly. All operating-system
interaction should remain inside `SystemService`.

---

## Version

- Plugin Version: **1.0.0**
- Compatible with: **Cipher v2+**