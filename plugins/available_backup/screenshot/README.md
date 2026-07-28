# Screenshot Plugin

The **Screenshot Plugin** allows Cipher v2 to capture screenshots on Ubuntu using natural language commands.

---

## Features

- Full-screen screenshots
- Active window screenshots
- Area/region selection screenshots
- Automatic save location
- Timestamped filenames
- Supports multiple screenshot backends

---

## Save Location

Screenshots are stored in:

```
~/Pictures/Cipher Screenshots/
```

Example filename:

```
2026-07-08_18-45-32.png
```

---

## Supported Commands

### Full Screen

- take a screenshot
- screenshot
- capture screen
- capture my screen
- take screen shot

---

### Active Window

- screenshot window
- capture current window
- capture active window
- take a window screenshot

---

### Area Selection

- screenshot area
- screenshot selection
- capture selected area
- select area screenshot

When supported by the backend (such as `gnome-screenshot -a`), the user will be able to interactively select the desired region.

---

## Supported Backends

Cipher automatically detects the first available utility.

Priority:

1. `gnome-screenshot`
2. `grim` (Wayland)

If no supported utility is available, the plugin returns an error instead of failing silently.

---

## Return Values

### Success

```python
{
    "success": True,
    "message": "Screenshot saved to /home/user/Pictures/Cipher Screenshots/2026-07-08_18-45-32.png",
    "path": "/home/user/Pictures/Cipher Screenshots/2026-07-08_18-45-32.png"
}
```

### Failure

```python
{
    "success": False,
    "message": "No supported screenshot utility found."
}
```

---

## Dependencies

Uses standard Linux utilities:

- `gnome-screenshot`
- `grim`

No additional Python packages are required.

---

## Future Enhancements

Planned features include:

- Delayed screenshots
- Multi-monitor capture
- Clipboard copy support
- OCR integration
- Instant annotation tools
- Automatic cloud upload
- Screen recording integration
- GIF capture
- Screenshot history
- AI-powered image understanding

---

Part of the **Cipher v2 Professional Ubuntu AI Assistant** plugin ecosystem.