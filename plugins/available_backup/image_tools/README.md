# Image Tools Plugin

The **Image Tools Plugin** provides common image manipulation utilities for Cipher v2. It is designed to support both user-facing image operations and internal workflows used by other plugins.

---

## Features

- Resize images
- Crop images
- Rotate images
- Convert image formats
- Generate thumbnails
- Read image metadata
- Validate supported image formats

---

## Supported Image Formats

| Format | Supported |
|---------|:---------:|
| PNG | ✅ |
| JPG | ✅ |
| JPEG | ✅ |
| BMP | ✅ |
| GIF | ✅ |
| TIFF | ✅ |
| WEBP | ✅ |

---

## Planned Voice Commands

Examples:

- resize this image
- crop image
- rotate photo
- convert image to PNG
- create thumbnail
- show image information
- image metadata

These requests will be handled through Cipher's structured image-intent pipeline.

---

## Public Methods

### Resize

```python
resize(
    source,
    destination,
    width,
    height
)
```

---

### Crop

```python
crop(
    source,
    destination,
    left,
    upper,
    right,
    lower
)
```

---

### Rotate

```python
rotate(
    source,
    destination,
    degrees
)
```

---

### Convert Format

```python
convert(
    source,
    destination
)
```

---

### Thumbnail

```python
thumbnail(
    source,
    destination,
    size=(256, 256)
)
```

---

### Metadata

```python
metadata(source)
```

Returns:

```python
{
    "format": "PNG",
    "mode": "RGB",
    "width": 1920,
    "height": 1080
}
```

---

## Dependencies

Python package:

- `Pillow`

Install:

```bash
pip install pillow
```

---

## Error Handling

The plugin reports errors when:

- Pillow is not installed
- the source image cannot be opened
- the image format is unsupported
- invalid image parameters are supplied

Exceptions are also logged through Cipher's logging system.

---

## Future Enhancements

Planned capabilities include:

- Image compression
- Watermarking
- EXIF editing
- Batch image processing
- Background removal
- AI-powered image enhancement
- OCR integration
- Face detection
- Object detection
- Color palette extraction
- Duplicate image detection

---

Part of the **Cipher v2 Professional Ubuntu AI Assistant** plugin ecosystem.