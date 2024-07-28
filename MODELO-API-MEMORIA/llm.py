from langchain_community.chat_models.ollama import ChatOllama


def get_llm():
    return ChatOllama(model="llama3", temperature=0)