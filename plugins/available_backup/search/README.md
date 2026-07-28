# Search Plugin

## Overview

The Search plugin enables Cipher to search the web and other searchable
resources through the centralized `SearchService`.

The plugin itself does **not** communicate with search engines or APIs.
Its responsibility is limited to:

- Detecting search-related commands
- Extracting the search query
- Delegating the request to `SearchService`
- Returning the formatted response

Keeping the plugin thin allows the search implementation to evolve
without changing the plugin.

---

## Features

- Web search
- Natural language search commands
- Query extraction
- Delegation to Cipher's Search Service

---

## Example Commands

### General Search

```text
search Python decorators
```

```text
search for Ubuntu keyboard shortcuts
```

```text
find machine learning tutorials
```

```text
look up OpenAI GPT
```

```text
lookup weather in Chennai
```

```text
google PyQt6 documentation
```

---

## Dependencies

This plugin depends on:

- `services.search_service`

---

## Required Permissions

- Network

---

## Architecture

```text
User
   │
   ▼
Search Plugin
   │
   ▼
SearchService
   │
   ├── Web Search Provider
   ├── Local Search Provider
   └── Future AI Search Providers
```

The plugin never performs HTTP requests directly. All networking,
provider selection, caching, ranking, and formatting should remain
inside `SearchService`.

---

## Future Enhancements

Potential future capabilities include:

- Search history
- Search suggestions
- Image search
- News search
- File search
- AI-powered semantic search
- Multiple search providers
- Result summarization

---

## Version

- Plugin Version: **1.0.0**
- Compatible with: **Cipher v2+**