from langchain_core.documents import Document
from src.ingestion.cleaner import clean_documents


def test_cleaner_preserves_metadata():
    long_text = "This is medically relevant content. " * 10

    docs = [
        Document(page_content=long_text, metadata={"page": 1}),
        Document(page_content=long_text, metadata={"page": 2}),
    ]

    cleaned = clean_documents(docs)

    assert len(cleaned) == 2
    assert cleaned[0].metadata["page"] == 1
    assert cleaned[1].metadata["page"] == 2