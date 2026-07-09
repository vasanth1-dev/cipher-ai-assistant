# Weather Plugin

## Overview

The Weather plugin enables Cipher to provide current weather information
by delegating all weather-related operations to Cipher's existing
`WeatherService`.

The plugin is intentionally lightweight. It is responsible only for:

- Detecting weather-related commands
- Extracting an optional location
- Calling the Weather Service
- Returning the formatted response

## Features

- Current weather
- Weather by city
- Natural language command detection
- Uses Cipher's central Weather Service

## Example Commands

### Current Location

```text
weather
```

```text
current weather
```

```text
what's the weather
```

### Specific Location

```text
weather in Chennai
```

```text
weather in London
```

```text
forecast in Tokyo
```

```text
what is the weather in New York
```

## Dependencies

This plugin depends on:

- `services.weather_service`

## Permissions

Required permissions:

- Network access

## Notes

The plugin does **not** communicate with external APIs directly.

All networking, caching, formatting, and provider-specific logic should
remain inside the Weather Service.

Keeping the plugin thin ensures:

- Easier testing
- Better maintainability
- Service reuse
- Cleaner architecture

## Version

- Plugin Version: **1.0.0**
- Compatible with: **Cipher v2+**