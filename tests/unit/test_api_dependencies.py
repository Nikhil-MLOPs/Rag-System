from src.api.dependencies import get_rag_chain


def test_rag_chain_is_cached():
    chain_1 = get_rag_chain()
    chain_2 = get_rag_chain()

    assert chain_1 is chain_2