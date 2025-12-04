from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_classic.memory import ConversationSummaryMemory
from langchain_core.runnables import RunnablePassthrough


# ----------------------------------------------------------
# 1. Global behavior (equivalent to a system message)
# ----------------------------------------------------------
GLOBAL_BEHAVIOR = """
You are a helpful, polite assistant.
Provide concise, non-repetitive, clear answers.
Do not ramble. Do not repeat ideas.
"""


# ----------------------------------------------------------
# 2. Your LLM
# ----------------------------------------------------------
llm_free_chat = OllamaLLM(
    model="mistral",
    temperature=0.2
)


# ----------------------------------------------------------
# 3. Summarizing memory (the new API still works)
# ----------------------------------------------------------
memory = ConversationSummaryMemory(
    llm=llm_free_chat,
    memory_key="chat_history",
    input_key="input"
)


# ----------------------------------------------------------
# 4. Prompt template
# ----------------------------------------------------------
TEMPLATE = """
{system_instructions}

Conversation so far:
{chat_history}

User: {input}
Assistant:
"""

prompt = PromptTemplate(
    template=TEMPLATE,
    input_variables=["input", "chat_history", "system_instructions"]
)


# ----------------------------------------------------------
# 5. Build runnable chain (new LangChain way)
# ----------------------------------------------------------
chat_chain = (
    {
        "input": RunnablePassthrough(),
        "chat_history": lambda _: memory.load_memory_variables({})["chat_history"],
        "system_instructions": lambda _: GLOBAL_BEHAVIOR
    }
    | prompt
    | llm_free_chat
)


# ----------------------------------------------------------
# 6. Call function that ALSO stores memory
# ----------------------------------------------------------
def ask_ai(user_input: str):
    # run model
    answer = chat_chain.invoke(user_input)

    # save memory (LangChain requires manual saving in runnable pipelines)
    memory.save_context(
        {"input": user_input},
        {"output": answer}
    )

    return answer


# ----------------------------------------------------------
# TEST
# ----------------------------------------------------------
# print(ask_ai("Hi, I'm 58 and want better health."))
# print(ask_ai("What did I say about my age?"))
# print(ask_ai("And what do you recommend next?"))
