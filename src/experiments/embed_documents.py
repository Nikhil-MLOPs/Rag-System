import logging
from pathlib import Path
from math import ceil
import yaml

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

from src.experiments.chunk_documents import chunk_documents
from src.core.logging.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

CONFIG_PATH = Path("configs/embeddings.yaml")

def batch(iterable, size):
    for i in range(0, len(iterable), size):
        yield iterable[i : i + size]

def run():
    config = yaml.safe_load(CONFIG_PATH.read_text())

    embed_cfg = config["embedding"]
    vs_cfg = config["vectorstore"]

    embeddings = OllamaEmbeddings(model=embed_cfg["model"])

    vectorstore = Chroma(
        collection_name=embed_cfg["collection_name"],
        persist_directory=vs_cfg["persist_directory"],
        embedding_function=embeddings,
    )

    for exp in config["experiments"]:
        logger.info(f"Embedding experiment: {exp['name']}")

        chunks = chunk_documents(
            chunk_size=exp["chunk_size"],
            chunk_overlap=exp["chunk_overlap"],
        )

        total_batches = ceil(len(chunks) / embed_cfg["batch_size"])

        for idx, chunk_batch in enumerate(
            batch(chunks, embed_cfg["batch_size"]), start=1
        ):
            logger.info(
                f"Embedding batch {idx}/{total_batches} "
                f"(size={len(chunk_batch)})"
            )
            vectorstore.add_documents(chunk_batch)

    logger.info("Embedding pipeline completed successfully")

if __name__ == "__main__":
    run()