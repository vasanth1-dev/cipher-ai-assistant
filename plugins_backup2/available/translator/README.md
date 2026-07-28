# Translator Plugin

The **Translator Plugin** enables Cipher v2 to translate text between multiple languages. It is designed to be used by Cipher's intent pipeline as well as by other plugins and services.

---

## Features

- Translate text between supported languages
- Automatic source language detection
- List supported languages
- Programmatic API for other Cipher modules
- Optional pronunciation support (when available)

---

## Planned Voice Commands

Examples:

- translate this to Tamil
- translate to English
- convert this sentence to Hindi
- what is this in French
- translate from English to German

These natural-language requests will be handled through Cipher's structured intent pipeline.

---

## Example Usage

Translate with automatic source detection:

```python
result = plugin.translate(
    text="Hello, how are you?",
    target="ta"
)
```

Specify both source and target languages:

```python
result = plugin.translate(
    text="Bonjour",
    source="fr",
    target="en"
)
```

Example result:

```python
{
    "text": "Hello",
    "source": "fr",
    "target": "en",
    "original": "Bonjour",
    "pronunciation": None
}
```

---

## Public Methods

- `translate()`
- `supported_languages()`
- `is_supported()`

---

## Dependencies

Python package:

- `googletrans==4.0.2`

Install:

```bash
pip install googletrans==4.0.2
```

An active internet connection is generally required for translations.

---

## Error Handling

The plugin reports errors when:

- the translation library is not installed
- the requested language code is unsupported
- translation fails because of network or service issues

Errors are also written to Cipher's logging system.

---

## Future Enhancements

Planned capabilities include:

- Offline translation models
- AI-powered contextual translation
- Conversation translation mode
- Speech-to-speech translation
- Document translation
- OCR + translation pipeline
- Language auto-selection based on user preferences
- Translation history
- Custom glossary support
- Multiple translation provider support (LibreTranslate, DeepL, OpenAI, etc.)

---

Part of the **Cipher v2 Professional Ubuntu AI Assistant** plugin ecosystem.