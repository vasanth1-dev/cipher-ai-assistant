# Notification Plugin

## Overview

The Notification plugin enables Cipher to display and manage desktop
notifications through the centralized `NotificationService`.

The plugin itself never interacts directly with the operating system's
notification APIs. Its responsibilities are limited to:

- Detecting notification-related commands
- Parsing notification messages
- Delegating requests to `NotificationService`
- Returning formatted responses

Keeping the plugin lightweight ensures that all notification logic,
platform integration, and history management remain centralized.

---

## Features

- Display desktop notifications
- Show custom notification messages
- Clear active notifications
- Dismiss all notifications
- View notification history

---

## Example Commands

### Show Notification

```text
notify Meeting starts in 10 minutes
```

```text
show notification Backup completed successfully
```

```text
notification System update available
```

---

### Manage Notifications

```text
clear notifications
```

```text
dismiss notifications
```

```text
notification history
```

---

## Dependencies

This plugin depends on:

- `services.notification_service`

---

## Required Permissions

- Notifications

---

## Architecture

```text
User
   │
   ▼
Notification Plugin
   │
   ▼
NotificationService
   │
   ▼
Desktop Notification System
```

All platform-specific notification APIs, persistence, scheduling,
priorities, icons, and history management should remain inside
`NotificationService`.

---

## Future Enhancements

Potential future capabilities include:

- Notification priorities
- Rich notifications with icons
- Action buttons
- Scheduled notifications
- Progress notifications
- Notification grouping
- Cross-device notifications
- Notification sounds
- Do Not Disturb integration

---

## Version

- Plugin Version: **1.0.0**
- Compatible with: **Cipher v2+**