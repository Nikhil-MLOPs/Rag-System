from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings


def get_retriever(persist_directory: str, k: int):
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings,
    )

    return vectorstore.as_retriever(search_kwargs={"k": k})