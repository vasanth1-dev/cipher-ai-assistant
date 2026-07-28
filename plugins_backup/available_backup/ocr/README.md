# OCR Plugin

The **OCR Plugin** enables Cipher v2 to extract text from image files using Optical Character Recognition (OCR).

---

## Features

- Extract text from images
- Multiple image format support
- Language selection
- Image validation
- Reusable API for other Cipher plugins
- Integration-ready for screenshots, camera captures, and scanned documents

---

## Supported Image Formats

| Format | Supported |
|---------|:---------:|
| PNG | ✅ |
| JPG | ✅ |
| JPEG | ✅ |
| BMP | ✅ |
| TIFF | ✅ |
| TIF | ✅ |
| WEBP | ✅ |

---

## Planned Voice Commands

Examples:

- read text from this image
- extract text from image
- perform OCR
- scan this document
- recognize text
- convert image to text

These commands will be connected through Cipher's document and image intent pipeline.

---

## Example Usage

```python
text = plugin.extract_text(
    Path("invoice.png")
)
```

Specify a language:

```python
text = plugin.extract_text(
    Path("receipt.jpg"),
    language="eng"
)
```

---

## Public Methods

- `extract_text()`
- `is_supported()`
- `exists()`

---

## Dependencies

Python packages:

- `pytesseract`
- `Pillow`

Install:

```bash
pip install pytesseract pillow
```

System package:

```bash
sudo apt install tesseract-ocr
```

Additional language packs can be installed as needed, for example:

```bash
sudo apt install tesseract-ocr-tam
```

for Tamil OCR support.

---

## Error Handling

The plugin reports errors when:

- OCR dependencies are not installed
- the image file does not exist
- the image format is unsupported
- OCR processing fails

Errors are also logged using Cipher's logging system.

---

## Future Enhancements

Planned capabilities include:

- Multi-language OCR
- Automatic language detection
- Handwriting recognition
- Table extraction
- Receipt and invoice parsing
- QR code recognition
- Barcode scanning
- Layout analysis
- OCR confidence scoring
- PDF OCR integration
- AI-powered document understanding

---

Part of the **Cipher v2 Professional Ubuntu AI Assistant** plugin ecosystem.