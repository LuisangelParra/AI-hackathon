from fastapi import FastAPI
from pydantic import BaseModel
from llm import get_llm
from prompt import get_chat_prompt_template
from chain import create_chain

app = FastAPI()

# Initialize the model, prompt, and chain
llm = get_llm()
prompt = get_chat_prompt_template()
chain = create_chain(llm, prompt)

class Question(BaseModel):
    content: str

@app.post("/ask")
def ask_question(question: Question):
    response = chain.invoke({"content": question.content})
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
