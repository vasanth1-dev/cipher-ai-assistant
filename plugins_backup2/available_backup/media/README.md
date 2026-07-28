# Media Plugin

## Overview

The Media plugin allows Cipher to control music and media playback
through the centralized `MediaService`.

The plugin itself contains no media-player-specific implementation.
Its responsibilities are limited to:

- Detecting media-related commands
- Extracting media names when required
- Delegating requests to `MediaService`
- Returning formatted responses

This architecture keeps the plugin lightweight while allowing the
underlying media implementation to evolve independently.

---

## Features

- Play media
- Pause playback
- Resume playback
- Stop playback
- Next track
- Previous track
- Shuffle
- Repeat
- Mute media
- Unmute media

---

## Example Commands

### Playback

```text
play Believer
```

```text
play relaxing music
```

```text
pause
```

```text
resume
```

```text
stop
```

---

### Navigation

```text
next
```

```text
previous
```

---

### Playback Modes

```text
shuffle
```

```text
repeat
```

---

### Audio

```text
mute music
```

```text
unmute music
```

---

## Dependencies

This plugin depends on:

- `services.media_service`

---

## Required Permissions

- Audio

---

## Architecture

```text
User
   │
   ▼
Media Plugin
   │
   ▼
MediaService
   │
   ├── Local Media Player
   ├── Streaming Services
   └── Future Media Providers
```

The plugin never communicates directly with a media player. All playback
control, player integration, device selection, and provider-specific
logic should remain inside `MediaService`.

---

## Future Enhancements

Potential future capabilities include:

- Playlist management
- Queue management
- Volume control
- Seek forward/backward
- Album and artist search
- Podcast support
- Voice-controlled playlists
- Multiple media provider support
- Smart recommendations

---

## Version

- Plugin Version: **1.0.0**
- Compatible with: **Cipher v2+**