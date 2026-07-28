# Text-to-Speech Plugin

The **Text-to-Speech Plugin** provides speech synthesis capabilities for Cipher v2. It can speak text aloud, save synthesized speech to audio files, and manage voice settings.

---

## Features

- Speak text aloud
- Save speech to an audio file
- Enumerate available voices
- Change active voice
- Configure speech rate
- Configure output volume

---

## Planned Voice Commands

Examples:

- read this aloud
- speak this text
- convert text to speech
- save speech to file
- change voice
- increase speaking speed

These requests will be routed through Cipher's structured speech-intent pipeline.

---

## Public Methods

### Speak Text

```python
speak(text)
```

Speaks the supplied text immediately.

---

### Save Speech

```python
save_to_file(
    text,
    output
)
```

Example:

```python
plugin.save_to_file(
    "Welcome to Cipher.",
    Path("welcome.mp3")
)
```

> The output format depends on the speech engine and platform capabilities.

---

### Available Voices

```python
voices()
```

Returns:

```python
[
    {
        "id": "...",
        "name": "English",
        "languages": [...]
    }
]
```

---

### Configure Voice

```python
set_voice(voice_id)
set_rate(180)
set_volume(0.9)
```

---

## Dependencies

Python package:

- `pyttsx3`

Install:

```bash
pip install pyttsx3
```

The plugin uses the native speech engine available on the operating system.

---

## Error Handling

The plugin reports errors when:

- `pyttsx3` is unavailable
- speech synthesis fails
- an invalid voice is selected

Exceptions are also logged through Cipher's logging system.

---

## Future Enhancements

Planned capabilities include:

- Neural voices
- Voice cloning
- SSML support
- Streaming speech output
- Multi-language voice selection
- Emotion-aware speech synthesis
- Speech caching
- AI-generated pronunciation improvements
- Integration with Cipher conversation history
- Voice profile management

---

Part of the **Cipher v2 Professional Ubuntu AI Assistant** plugin ecosystem.