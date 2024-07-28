from langchain.chains.llm import LLMChain
from memory import get_memory

def create_chain(llm, prompt):
    return LLMChain(llm=llm, prompt=prompt, memory=get_memory())

def memory():
    return get_memory()
