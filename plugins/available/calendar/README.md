# Calendar Plugin

## Overview

The Calendar plugin enables Cipher to create, manage, and view calendar
events through the centralized `CalendarService`.

The plugin itself contains no calendar provider implementation. Its
responsibilities are limited to:

- Detecting calendar-related commands
- Parsing user requests
- Delegating operations to `CalendarService`
- Returning formatted responses

This architecture keeps all scheduling logic centralized and reusable.

---

## Features

- Create calendar events
- Schedule meetings
- View today's events
- List upcoming events
- Delete events
- Natural language calendar commands

---

## Example Commands

### Create Events

```text
create event Team meeting tomorrow at 10 AM
```

```text
add event Doctor appointment on Friday at 5 PM
```

---

### Schedule Meetings

```text
schedule meeting with John tomorrow at 3 PM
```

---

### View Calendar

```text
calendar
```

```text
show calendar
```

```text
today events
```

```text
show events
```

```text
list events
```

---

### Delete Events

```text
delete event Team meeting
```

---

## Dependencies

This plugin depends on:

- `services.calendar_service`

---

## Required Permissions

- Network

---

## Architecture

```text
User
   │
   ▼
Calendar Plugin
   │
   ▼
CalendarService
   │
   ├── Local Calendar
   ├── Google Calendar
   ├── Microsoft Outlook
   └── Future Calendar Providers
```

The plugin never communicates with calendar providers directly. All
authentication, synchronization, recurrence handling, reminders, and
provider-specific logic should remain inside `CalendarService`.

---

## Future Enhancements

Potential future capabilities include:

- Google Calendar synchronization
- Outlook Calendar integration
- Recurring events
- Event reminders
- Time zone support
- Shared calendars
- Meeting invitations
- Availability checking
- AI-assisted schedule planning

---

## Version

- Plugin Version: **1.0.0**
- Compatible with: **Cipher v2+**