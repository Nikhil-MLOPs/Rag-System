from langchain_core.documents import Document
from src.experiments.chunk_documents import chunk_from_documents


def test_chunking_produces_chunks():
    docs = [
        Document(
            page_content="This is medically relevant content. " * 10,
            metadata={"page": 1},
        )
    ]

    chunks = chunk_from_documents(
        documents=docs,
        chunk_size=200,
        chunk_overlap=50,
    )

    assert len(chunks) > 0


def test_chunk_metadata_present():
    docs = [
        Document(
            page_content="Medical information content. " * 10,
            metadata={"page": 2},
        )
    ]

    chunks = chunk_from_documents(
        documents=docs,
        chunk_size=200,
        chunk_overlap=50,
    )

    chunk = chunks[0]
    assert chunk.metadata["page"] == 2
    assert chunk.metadata["chunk_size"] == 200
    assert chunk.metadata["chunk_overlap"] == 50