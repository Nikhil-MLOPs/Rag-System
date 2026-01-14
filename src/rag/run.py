import yaml
from pathlib import Path

from src.rag.retriever import get_retriever
from src.rag.prompt import build_prompt
from src.rag.chain import build_rag_chain

CONFIG_PATH = Path("configs/rag.yaml")


def run(question: str):
    config = yaml.safe_load(CONFIG_PATH.read_text())

    retriever = get_retriever(
        persist_directory="data/vectorstore/chroma",
        k=config["retriever"]["k"],
    )

    prompt = build_prompt(
        config["prompt"]["system"],
        config["prompt"]["human"],
    )

    chain = build_rag_chain(
        prompt=prompt,
        retriever=retriever,
        model_name=config["llm"]["model"],
        temperature=config["llm"]["temperature"],
    )

    return chain.invoke(question)