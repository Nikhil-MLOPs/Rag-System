from src.rag.prompt import build_prompt


def test_prompt_builds():
    prompt = build_prompt("system", "human")
    assert prompt is not None