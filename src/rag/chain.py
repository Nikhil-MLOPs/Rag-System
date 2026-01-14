from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser


def build_rag_chain(prompt, retriever, model_name: str, temperature: float):
    llm = ChatOllama(
        model=model_name,
        temperature=temperature,
    )

    def format_docs(docs):
        return "\n\n".join(
            f"[PAGE={doc.metadata.get('page')}] {doc.page_content}"
            for doc in docs
        )

    chain = (
        {
            "context": retriever | format_docs,
            "question": lambda x: x,
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain