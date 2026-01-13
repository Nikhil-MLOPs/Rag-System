from src.experiments.chunk_documents import chunk_documents

def test_chunking_produces_chunks():
    chunks = chunk_documents(chunk_size=500, chunk_overlap=100)
    assert len(chunks) > 0

def test_chunk_metadata_present():
    chunks = chunk_documents(chunk_size=500, chunk_overlap=100)
    assert "page" in chunks[0].metadata
    assert "chunk_size" in chunks[0].metadata
    assert "chunk_overlap" in chunks[0].metadata