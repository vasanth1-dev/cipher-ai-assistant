# Brightness Plugin

The **Brightness Plugin** allows Cipher v2 to control the display brightness on Ubuntu using natural language commands.

---

## Features

- Increase brightness
- Decrease brightness
- Set brightness to a specific percentage
- View the current brightness level
- Automatic backend detection
- Safe percentage validation (1–100%)

---

## Supported Backends

Cipher automatically detects and uses the first available backend.

Priority:

1. `brightnessctl` (recommended)
2. `xrandr` (future support)

> **Note:** The current implementation provides full functionality through `brightnessctl`. Detection for `xrandr` is included for future expansion.

---

## Supported Commands

### Increase Brightness

Examples:

- increase brightness
- brightness up
- raise brightness
- increase brightness by 10 percent

---

### Decrease Brightness

Examples:

- decrease brightness
- brightness down
- lower brightness
- reduce brightness by 20 percent

---

### Set Brightness

Examples:

- set brightness to 50 percent
- set brightness 75
- brightness 30 percent

---

### Current Brightness

Examples:

- current brightness
- brightness status
- what is the current brightness
- check screen brightness

---

## Return Values

### Success

```python
{
    "success": True,
    "message": "Brightness increased by 10%."
}
```

Current brightness query:

```python
{
    "success": True,
    "message": "Current brightness is 65%.",
    "brightness": 65
}
```

### Failure

```python
{
    "success": False,
    "message": "No supported brightness backend found."
}
```

---

## Dependencies

The plugin relies on standard Linux utilities.

Recommended:

- `brightnessctl`

Future backend:

- `xrandr`

Install `brightnessctl` if needed:

```bash
sudo apt install brightnessctl
```

---

## Security

- Brightness values are restricted to **1–100%**.
- Invalid values are automatically clamped to the supported range.
- The plugin only changes display brightness and does not modify monitor configuration.

---

## Future Enhancements

Planned capabilities include:

- Multi-monitor brightness control
- External monitor support via DDC/CI
- Automatic brightness profiles
- Night mode integration
- Ambient light sensor support
- Time-based brightness scheduling
- Battery-aware brightness optimization
- Voice confirmation for brightness changes
- GUI brightness slider synchronization
- Adaptive brightness using AI

---

Part of the **Cipher v2 Professional Ubuntu AI Assistant** plugin ecosystem.