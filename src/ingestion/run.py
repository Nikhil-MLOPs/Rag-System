import logging
from pathlib import Path

from src.core.logging.logging_config import setup_logging
from src.ingestion.pdf_loader import load_pdf
from src.ingestion.cleaner import clean_documents

setup_logging()
logger = logging.getLogger(__name__)

RAW_PDF = Path("data/raw/Medical-book.pdf")
OUTPUT_FILE = Path("data/processed/cleaned_documents.txt")

def run():
    logger.info("Starting PDF ingestion pipeline")

    documents = load_pdf(RAW_PDF)
    cleaned_documents = clean_documents(documents)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        for doc in cleaned_documents:
            page = doc.metadata.get("page", "unknown")
            f.write(f"[PAGE={page}]\n")
            f.write(doc.page_content)
            f.write("\n\n")

    logger.info("PDF ingestion and cleaning completed successfully")

if __name__ == "__main__":
    run()