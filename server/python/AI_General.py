from langchain_ollama import OllamaLLM
from langchain_classic.agents import initialize_agent, Tool

# https://chatgpt.com/c/69206897-d7fc-832b-be9d-ae571539cd6a

# Creative LLM for general chat
llm_free_chat = OllamaLLM(model="mistral", temperature=0.2)


# function to export:
# --------------------
def ask_ai(prompt_ai: str):
    clean_prompt = prompt_ai.strip()
    if len(clean_prompt) == 0:
        return "No prompt received."
    else:
        return llm_free_chat.invoke("Provide a concise, non-repetitive, clear answer.\n" + clean_prompt)
    


# print(ask_ai("Hello. In what year was the current King of England born?"))