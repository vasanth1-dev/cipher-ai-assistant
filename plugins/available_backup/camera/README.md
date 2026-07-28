# Camera Plugin

The **Camera Plugin** allows Cipher v2 to capture photos from the system's default webcam using natural language commands.

---

## Features

- Capture a photo from the default camera
- Automatic timestamped filenames
- Automatic photo storage directory creation
- Multiple backend support
- No external Python dependencies

---

## Save Location

Captured images are stored in:

```text
~/Pictures/Cipher Camera/
```

Example filename:

```text
2026-07-08_18-45-32.jpg
```

---

## Supported Commands

Examples:

- take a photo
- take picture
- capture photo
- capture image
- open camera
- use webcam
- take selfie
- camera

---

## Supported Backends

Cipher automatically detects the first available backend.

Priority:

1. `fswebcam`
2. `ffmpeg`

If neither backend is available, the plugin returns an error.

---

## Example Response

### Success

```python
{
    "success": True,
    "message": "Photo saved to /home/user/Pictures/Cipher Camera/2026-07-08_18-45-32.jpg",
    "path": "/home/user/Pictures/Cipher Camera/2026-07-08_18-45-32.jpg"
}
```

### Failure

```python
{
    "success": False,
    "message": "No supported camera utility found. Install fswebcam or ffmpeg."
}
```

---

## Dependencies

Supported Linux utilities:

- `fswebcam` (recommended)
- `ffmpeg`

Example installation:

```bash
sudo apt install fswebcam
```

or

```bash
sudo apt install ffmpeg
```

---

## Notes

- Uses the default camera device (`/dev/video0`) when using the `ffmpeg` backend.
- The plugin captures a single still image and exits immediately.
- The destination directory is created automatically if it does not already exist.

---

## Future Enhancements

Planned capabilities include:

- Live camera preview
- Multiple camera selection
- Video recording
- Burst photo mode
- Countdown timer
- Face detection
- QR code scanning
- Barcode recognition
- AI image captioning
- OCR integration
- Camera settings (resolution, exposure, focus)
- Virtual camera support

---

Part of the **Cipher v2 Professional Ubuntu AI Assistant** plugin ecosystem.