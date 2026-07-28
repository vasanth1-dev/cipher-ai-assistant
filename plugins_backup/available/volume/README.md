# Volume Plugin

The **Volume Plugin** enables Cipher v2 to control the system audio volume using natural language commands on Ubuntu.

---

## Features

- Increase volume
- Decrease volume
- Set an exact volume percentage
- Mute audio
- Unmute audio
- Toggle mute
- Get the current volume level
- Automatic backend detection

---

## Supported Backends

Cipher automatically selects the first supported audio backend.

Priority:

1. `wpctl` (PipeWire)
2. `pactl` (PulseAudio)

No configuration is required.

---

## Supported Commands

### Increase Volume

Examples:

- increase volume
- volume up
- raise volume
- increase volume by 10 percent
- make it louder

---

### Decrease Volume

Examples:

- decrease volume
- volume down
- lower volume
- reduce volume by 20 percent
- make it quieter

---

### Set Volume

Examples:

- set volume to 50 percent
- set volume 75
- volume 30 percent

---

### Mute

Examples:

- mute
- mute audio
- mute speakers
- mute sound

---

### Unmute

Examples:

- unmute
- unmute audio
- restore sound

---

### Toggle Mute

Examples:

- toggle mute
- switch mute

---

### Current Volume

Examples:

- current volume
- volume status
- what is the current volume
- check audio volume

---

## Return Values

### Success

```python
{
    "success": True,
    "message": "Volume increased by 10%."
}
```

Current volume query:

```python
{
    "success": True,
    "message": "Current volume is Volume: 0.65.",
    "volume": "Volume: 0.65"
}
```

### Failure

```python
{
    "success": False,
    "message": "No supported audio backend found (wpctl or pactl)."
}
```

---

## Dependencies

The plugin uses standard Linux audio utilities:

- `wpctl` (PipeWire)
- `pactl` (PulseAudio)

No external Python packages are required.

---

## Future Enhancements

Planned capabilities include:

- Per-application volume control
- Microphone volume management
- Balance (left/right) adjustment
- Audio device switching
- Bluetooth audio device selection
- Volume profiles
- Automatic volume normalization
- Voice feedback after adjustments
- Media session integration
- AI-based smart volume suggestions

---

Part of the **Cipher v2 Professional Ubuntu AI Assistant** plugin ecosystem.