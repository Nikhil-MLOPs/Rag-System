def test_embedding_module_imports():
    from src.experiments.embed_documents import run
    assert callable(run)