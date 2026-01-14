def test_chain_builder_imports():
    from src.rag.chain import build_rag_chain
    assert callable(build_rag_chain)