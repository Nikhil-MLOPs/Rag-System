from pathlib import Path
from langchain_chroma import Chroma

def test_vectorstore_directory_exists():
    path = Path("data/vectorstore/chroma")
    assert path.exists()

def test_chroma_can_load():
    vs = Chroma(
        persist_directory="data/vectorstore/chroma",
        embedding_function=None,
    )
    assert vs is not None