# PDF Plugin

The **PDF Plugin** provides PDF document utilities for Cipher v2. It is designed to be used by the assistant's document-intent pipeline and can also be used programmatically by other plugins.

---

## Features

- Read PDF metadata
- Extract text from PDF documents
- Count the number of pages
- Merge multiple PDF files
- Split a PDF into individual pages
- Validate PDF files

---

## Supported Operations

### Read Metadata

Retrieve document metadata such as:

- Title
- Author
- Subject
- Creator
- Producer
- Creation date
- Modification date

---

### Extract Text

Extract text from every page in a PDF document.

Example:

```python
text = plugin.extract_text(Path("manual.pdf"))
```

---

### Page Count

Example:

```python
pages = plugin.page_count(Path("book.pdf"))
```

Returns:

```text
348
```

---

### Merge PDFs

Example:

```python
plugin.merge(
    [
        Path("chapter1.pdf"),
        Path("chapter2.pdf"),
        Path("chapter3.pdf")
    ],
    Path("book.pdf")
)
```

---

### Split PDF

Example:

```python
plugin.split(
    Path("report.pdf"),
    Path("./pages")
)
```

Output:

```text
pages/
├── page_1.pdf
├── page_2.pdf
├── page_3.pdf
...
```

---

## Planned Voice Commands

Examples:

- read this pdf
- merge these pdf files
- split this pdf
- extract text from pdf
- how many pages are in this pdf
- show pdf metadata

These commands will be connected to Cipher's structured document processing pipeline.

---

## Dependencies

Python package:

- `pypdf`

Install:

```bash
pip install pypdf
```

---

## Public Methods

- `page_count()`
- `extract_text()`
- `metadata()`
- `merge()`
- `split()`
- `is_pdf()`
- `exists()`

---

## Error Handling

The plugin reports errors when:

- the PDF library is unavailable
- the document cannot be opened
- the document is corrupted
- the file does not exist

Errors are also written to Cipher's logging system.

---

## Future Enhancements

Planned capabilities include:

- Password-protected PDF support
- PDF encryption and decryption
- Rotate pages
- Delete pages
- Rearrange pages
- Watermark support
- Image extraction
- OCR integration for scanned PDFs
- PDF compression
- PDF-to-image conversion
- AI-powered document summarization

---

Part of the **Cipher v2 Professional Ubuntu AI Assistant** plugin ecosystem.