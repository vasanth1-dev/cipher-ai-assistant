# Reminder Plugin

## Overview

The Reminder plugin allows Cipher to create, manage, and track reminders.

It integrates with Cipher's existing `ReminderService` and `TimeParser`
instead of implementing its own reminder storage, ensuring all reminders
are managed consistently across the application.

## Features

- Create reminders
- List all reminders
- Complete reminders
- Delete reminders
- Natural language time parsing
- Uses Cipher's central reminder service

## Example Commands

### Create

```text
Remind me to call John at 6 PM
```

```text
Set reminder to submit my assignment tomorrow at 9 AM
```

```text
Add reminder to pay electricity bill on Friday
```

### View

```text
Show reminders
```

```text
List reminders
```

```text
My reminders
```

### Complete

```text
Complete reminder 2
```

### Delete

```text
Delete reminder 3
```

## Dependencies

This plugin depends on the following Cipher services:

- `services.reminder_service`
- `services.time_parser`

## Notes

- Reminder scheduling is handled by Cipher's Reminder Service.
- Time parsing is delegated to the central Time Parser.
- The plugin itself only interprets user commands and forwards them to the appropriate services.

## Version

- Plugin Version: **1.0.0**
- Compatible with: **Cipher v2+**