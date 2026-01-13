import logging
import re
from typing import List

from langchain_core.documents import Document

logger = logging.getLogger(__name__)

def clean_documents(documents: List[Document]) -> List[Document]:
    cleaned_docs = []

    for doc in documents:
        text = doc.page_content

        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"\n{2,}", "\n", text)
        text = text.strip()

        if len(text) < 50:
            continue

        cleaned_docs.append(
            Document(
                page_content=text,
                metadata=doc.metadata,
            )
        )

    logger.info(f"Documents after cleaning: {len(cleaned_docs)}")
    return cleaned_docs