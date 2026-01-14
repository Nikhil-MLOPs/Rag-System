import logging
from pathlib import Path
from typing import List

import yaml
import mlflow
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.core.config.mlflow_config import setup_mlflow

logger = logging.getLogger(__name__)

CLEANED_DOC_PATH = Path("data/processed/cleaned_documents.txt")
CONFIG_PATH = Path("configs/chunking.yaml")

def load_cleaned_documents() -> List[Document]:
    documents = []
    current_page = None
    buffer = []

    with CLEANED_DOC_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("[PAGE="):
                if buffer and current_page is not None:
                    documents.append(
                        Document(
                            page_content="".join(buffer).strip(),
                            metadata={"page": current_page},
                        )
                    )
                    buffer = []

                current_page = int(line.replace("[PAGE=", "").replace("]\n", ""))
            else:
                buffer.append(line)

    if buffer and current_page is not None:
        documents.append(
            Document(
                page_content="".join(buffer).strip(),
                metadata={"page": current_page},
            )
        )

    logger.info(f"Loaded {len(documents)} cleaned page-level documents")
    return documents

def chunk_from_documents(documents: list[Document], chunk_size: int, chunk_overlap: int,) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap,)

    chunks = splitter.split_documents(documents)

    for chunk in chunks:
        chunk.metadata["chunk_size"] = chunk_size
        chunk.metadata["chunk_overlap"] = chunk_overlap

    return chunks

def chunk_documents(chunk_size: int, chunk_overlap: int) -> list[Document]:
    documents = load_cleaned_documents()
    return chunk_from_documents(documents, chunk_size, chunk_overlap)

def run():
    setup_mlflow()

    config = yaml.safe_load(CONFIG_PATH.read_text())
    experiments = config["experiments"]

    for exp in experiments:
        with mlflow.start_run(run_name=exp["name"]):
            chunk_size = exp["chunk_size"]
            chunk_overlap = exp["chunk_overlap"]

            logger.info(f"Running experiment: {exp['name']}")

            chunks = chunk_documents(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
            )

            avg_chunk_length = sum(
                len(chunk.page_content) for chunk in chunks
            ) / len(chunks)

            mlflow.log_param("chunk_size", chunk_size)
            mlflow.log_param("chunk_overlap", chunk_overlap)
            mlflow.log_metric("num_chunks", len(chunks))
            mlflow.log_metric("avg_chunk_length", avg_chunk_length)

            logger.info(
                f"Experiment {exp['name']} | "
                f"chunks={len(chunks)} | "
                f"avg_len={avg_chunk_length:.2f}"
            )

if __name__ == "__main__":
    run()