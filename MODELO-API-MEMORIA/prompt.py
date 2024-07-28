from langchain.prompts import (
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)


def get_chat_prompt_template():
    return ChatPromptTemplate(
        input_variables=["content", "messages"],
        messages=[
            SystemMessagePromptTemplate.from_template(
                """
                    You are a helpful ai assistent.
                    try to answer the questions to the best of your knowledge
                """
            ),
            MessagesPlaceholder(variable_name="messages"),
            HumanMessagePromptTemplate.from_template("{content}"),
        ],
    )