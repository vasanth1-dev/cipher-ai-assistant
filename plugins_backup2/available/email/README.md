# Email Plugin

## Overview

The Email plugin enables Cipher to compose, send, read, and manage
emails through the centralized `EmailService`.

The plugin itself does not communicate directly with email providers.
Its responsibilities are limited to:

- Detecting email-related commands
- Parsing user requests
- Delegating operations to `EmailService`
- Returning formatted responses

This architecture keeps all provider-specific logic inside the service
layer.

---

## Features

- Compose emails
- Send emails
- Save draft emails
- Read recent emails
- Check inbox
- Natural language email commands

---

## Example Commands

### Send Email

```text
send email to john@example.com saying Meeting is at 3 PM
```

```text
email alice@example.com Hello, how are you?
```

---

### Compose

```text
compose email to manager@example.com
```

---

### Draft

```text
draft email about project update
```

---

### Read Mail

```text
read emails
```

```text
check email
```

```text
check inbox
```

```text
show inbox
```

---

## Dependencies

This plugin depends on:

- `services.email_service`

---

## Required Permissions

- Network

---

## Architecture

```text
User
   │
   ▼
Email Plugin
   │
   ▼
EmailService
   │
   ├── SMTP
   ├── IMAP
   └── Future Email Providers
```

The plugin never handles authentication, SMTP, IMAP, OAuth, or network
communication directly. Those responsibilities belong entirely to
`EmailService`.

---

## Future Enhancements

Potential future capabilities include:

- Gmail OAuth integration
- Outlook integration
- Attachment support
- HTML email composition
- Contact lookup
- Email search
- Spam filtering
- Scheduled email sending
- AI-assisted email drafting and summarization

---

## Version

- Plugin Version: **1.0.0**
- Compatible with: **Cipher v2+**