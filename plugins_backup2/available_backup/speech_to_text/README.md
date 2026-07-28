# Speech-to-Text Plugin

The **Speech-to-Text Plugin** provides offline speech recognition for Cipher v2 using Faster-Whisper. It is designed for transcription workflows and integration with Cipher's voice assistant.

---

## Features

- Offline speech recognition
- Audio file transcription
- Language selection
- Timestamped transcription segments
- Reusable API for other Cipher components
- Faster-Whisper backend

---

## Planned Voice Commands

Examples:

- transcribe this audio
- convert speech to text
- audio to text
- recognize speech
- transcribe recording

These requests will be routed through Cipher's structured speech-intent pipeline.

---

## Public Methods

### Load Model

```python
load_model(
    model_name="base.en",
    device="cpu",
    compute_type="int8"
)
```

Example model names:

- tiny
- base
- base.en
- small
- medium
- large-v3

---

### Transcribe

```python
transcribe(
    Path("meeting.wav"),
    language="en"
)
```

Returns:

```python
{
    "text": "Hello everyone, welcome to today's meeting.",
    "language": "en",
    "duration": 12.6,
    "segments": [
        {
            "start": 0.0,
            "end": 3.2,
            "text": "Hello everyone,"
        }
    ]
}
```

---

## Dependencies

Python package:

- `faster-whisper`

Install:

```bash
pip install faster-whisper
```

Depending on your platform, additional runtime libraries for CTranslate2 may also be required.

---

## Integration

This plugin is intended to complement Cipher's existing voice pipeline. It can be reused for:

- Audio file transcription
- Voice notes
- Meeting transcription
- Subtitle generation
- Offline speech recognition tasks

---

## Error Handling

The plugin reports errors when:

- Faster-Whisper is unavailable
- the speech model has not been loaded
- the audio file cannot be found
- transcription fails

Exceptions are also logged through Cipher's logging system.

---

## Future Enhancements

Planned capabilities include:

- Real-time streaming transcription
- Speaker diarization
- Automatic language detection
- Subtitle (SRT/VTT) generation
- Translation during transcription
- Noise reduction preprocessing
- GPU optimization
- Wake-word integration
- Conversation memory integration
- AI-generated transcript summaries

---

Part of the **Cipher v2 Professional Ubuntu AI Assistant** plugin ecosystem.