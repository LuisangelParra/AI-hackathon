from langchain.memory.buffer import ConversationBufferMemory
from langchain.memory.chat_message_histories.file import FileChatMessageHistory


def get_memory():
    return ConversationBufferMemory(
        memory_key="messages",
        chat_memory=FileChatMessageHistory(file_path="memory.json"),
        return_messages=True,
        input_key="content",
    )