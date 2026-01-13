from pathlib import Path

from src.ingestion.pdf_loader import load_pdf

def test_pdf_loads():
    path = Path("data/raw/Medical-book.pdf")
    docs = load_pdf(path)
    assert len(docs) > 0