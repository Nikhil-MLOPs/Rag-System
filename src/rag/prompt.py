from langchain_core.prompts import ChatPromptTemplate


def build_prompt(system_prompt: str, human_prompt: str):
    return ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", human_prompt),
        ]
    )