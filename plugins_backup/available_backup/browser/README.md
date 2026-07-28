# Browser Plugin

## Overview

The Browser plugin enables Cipher to open websites, URLs, and perform
browser-related actions through the centralized `BrowserService`.

The plugin itself does not interact with browsers directly. Its
responsibilities are limited to:

- Detecting browser-related commands
- Extracting URLs or search targets
- Delegating requests to `BrowserService`
- Returning formatted responses

This design keeps browser integration centralized and platform-independent.

---

## Features

- Open websites
- Open URLs
- Browse web pages
- Open domains
- Natural language browser commands

---

## Example Commands

### Open Websites

```text
open https://www.python.org
```

```text
open github.com
```

```text
visit openai.com
```

```text
go to stackoverflow.com
```

---

### Browse

```text
browse ChatGPT
```

```text
browse Ubuntu documentation
```

---

### URLs

```text
open url https://docs.python.org
```

```text
open website example.com
```

---

## Dependencies

This plugin depends on:

- `services.browser_service`

---

## Required Permissions

- Network

---

## Architecture

```text
User
   │
   ▼
Browser Plugin
   │
   ▼
BrowserService
   │
   ▼
Default Web Browser
```

All browser launching, URL validation, search engine selection,
platform-specific integration, and error handling should remain inside
`BrowserService`.

---

## Future Enhancements

Potential future capabilities include:

- Browser history
- Bookmark management
- Open multiple tabs
- Close tabs
- Incognito mode
- Download manager
- Browser profile selection
- Voice-driven navigation
- AI-assisted web browsing

---

## Version

- Plugin Version: **1.0.0**
- Compatible with: **Cipher v2+**