# QR Code Plugin

The **QR Code Plugin** enables Cipher v2 to generate and decode QR codes. It can be used by the assistant, other plugins, and future GUI tools.

---

## Features

- Generate QR codes from text
- Decode QR codes from image files
- Automatic output directory creation
- PNG image generation
- Reusable API for other Cipher components

---

## Output Directory

Generated QR codes are stored in:

```text
~/Pictures/Cipher QR Codes/
```

Example:

```text
~/Pictures/Cipher QR Codes/contact.png
```

---

## Planned Voice Commands

Examples:

- generate QR code
- create QR code
- make a QR for this URL
- scan QR code
- decode this QR image
- read QR code

These commands will be connected through Cipher's structured image-intent pipeline.

---

## Public Methods

### Generate

```python
generate(
    text,
    filename
)
```

Example:

```python
plugin.generate(
    "https://example.com",
    "website"
)
```

Creates:

```text
website.png
```

---

### Decode

```python
decode(
    Path("code.png")
)
```

Returns:

```python
[
    "https://example.com"
]
```

---

## Dependencies

Python packages:

- `qrcode[pil]`
- `Pillow`
- `pyzbar`

Install:

```bash
pip install qrcode[pil] pillow pyzbar
```

Linux dependency (required by `pyzbar`):

```bash
sudo apt install libzbar0
```

---

## Error Handling

The plugin reports errors when:

- QR generation libraries are unavailable
- QR decoding libraries are unavailable
- the image cannot be opened
- no QR code is found in the image

Errors are also recorded through Cipher's logging system.

---

## Future Enhancements

Planned capabilities include:

- Batch QR generation
- Custom colors
- Embedded logos
- SVG output
- QR version selection
- Error-correction level selection
- Barcode generation
- Barcode decoding
- Webcam QR scanning
- Live camera scanning
- Wi-Fi QR code generation
- Contact (vCard) QR code generation

---

Part of the **Cipher v2 Professional Ubuntu AI Assistant** plugin ecosystem.