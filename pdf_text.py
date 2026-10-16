"""Day 4 (supplied): turn an uploaded PDF into plain text, in memory. The file is never saved."""
from pypdf import PdfReader
from pypdf.errors import PdfReadError

MAX_PAGES = 10
MAX_CHARACTERS = 6000  # Enough for a portfolio summary; keeps each AI request small.


def extract_text(upload):
    """upload is Flask's request.files.get(...). Return (text, problems)."""
    if upload is None or not upload.filename:
        return "", ["choose a PDF file"]
    if not upload.stream.read(5).startswith(b"%PDF-"):
        return "", ["the file is not a PDF"]
    upload.stream.seek(0)
    try:
        reader = PdfReader(upload.stream)
        if len(reader.pages) > MAX_PAGES:
            return "", [f"the PDF has more than {MAX_PAGES} pages"]
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    except PdfReadError:
        return "", ["the PDF could not be read"]
    lines = (" ".join(line.split()) for line in text.splitlines())  # No repeated spaces.
    text = "\n".join(line for line in lines if line)
    if not text:
        return "", ["no readable text: a scanned image has no text to read"]
    return text[:MAX_CHARACTERS], []
