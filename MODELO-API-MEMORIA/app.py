from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional
from llm import get_llm
from prompt import get_chat_prompt_template
from chain import create_chain

app = FastAPI()

# Initialize the model, prompt, and chain
llm = get_llm()
prompt = get_chat_prompt_template()
chain = create_chain(llm, prompt)

class Message(BaseModel):
    role: str
    content: str

class Question(BaseModel):
    content: str
    history: Optional[List[Message]] = Field(default=[])

@app.post("/ask")
def ask_question(question: Question):
    # Clear existing memory to handle new conversations
    # chain.memory.clear()

    # Load previous messages into the memory if provided
    if question.history:
        for message in question.history:
            if message.role == "user":
                chain.memory.chat_memory.add_user_message(message.content)
            elif message.role == "assistant":
                chain.memory.chat_memory.add_ai_message(message.content)
    
    # Get the response from the model
    response = chain.invoke({"content": question.content})
    
    # Save the new message into the history
    chain.memory.chat_memory.add_user_message(question.content)
    chain.memory.chat_memory.add_ai_message(response["text"])  # Assuming response is a dict with key 'text'

    return {"response": response["text"]}  # Return the response text directly

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
