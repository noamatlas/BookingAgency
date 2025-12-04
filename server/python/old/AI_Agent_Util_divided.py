from langchain_ollama import OllamaLLM
from langchain_classic.agents import initialize_agent, Tool
import re
from sql_util import run_query_sql
# https://chatgpt.com/c/69206897-d7fc-832b-be9d-ae571539cd6a

llm = OllamaLLM(model="mistral", temperature=0)
llm_free = OllamaLLM(model="mistral", temperature=0.8)
intent_llm = OllamaLLM(model="mistral", temperature=0)

def detect_intent(text: str):
    prompt = f"""
    Classify the user's message into one of two categories:
    - TRAVEL (if the user is asking about countries, destinations, flights, vacations)
    - GENERAL (anything else)

    User message: "{text}"

    Answer with only TRAVEL or GENERAL.
    """
    result = intent_llm.invoke(prompt)
    return result.strip().upper()




# ✅ TOOL 1 — Extract Country (LLM only):
# ----------------------------------------
def detect_country(text: str):
    prompt = f"""
    Extract the COUNTRY mentioned in this text.
    Return only the country name. Nothing else.
    If multiple appear, return the most relevant one.

    Text: {text}

    Country:
    """

    result = llm.invoke(prompt)
    cleaned = result.strip().replace(".", "").strip()
    return cleaned


# ✅ TOOL 2 — Get Valid Countries (SQL only):
# --------------------------------------------
def get_valid_countries(_ignored: str = ""): #Notice _ignored — Tools must take one string argument, so we allow it.
    rows = run_query_sql("SELECT DISTINCT destination FROM Vacations", "fetch")
    return [row[0] for row in rows]


# ✅ TOOL 3 — Get vacations for a specific country (SQL only):
# -------------------------------------------------------------
def get_vacations_by_country(country: str):
    country = country.strip().replace("'", "''")
    query = f"SELECT * FROM Vacations WHERE destination LIKE '{country}%' ORDER BY startDate"
    rows = run_query_sql(query, "fetch")
    return rows

# ✅ TOOL 4 — summarize_vacation_record:
# ---------------------------------------
def summarize_vacation(record: str):
    prompt = f"""
    Convert this raw SQL vacation record into a friendly description.

    Record:
    {record}

    Summary:
    """
    return llm.invoke(prompt).strip()


# ⭐ REGISTER TOOLS:
# -------------------
tools = [
    Tool(name="detect_country", 
         func=detect_country,
         description="Extract the country name from user text."),    
    Tool(name="list_countries", 
         func=get_valid_countries,
         description="Get all valid vacation countries."),
    Tool(name="vacations_for_country", 
         func=get_vacations_by_country,
         description="Get vacations for a given country name."),
    Tool(name="detect_intent", 
         func=detect_intent,
         description="Classify a text as TRAVEL or GENERAL.")
]


# ⭐ AGENT SETUP:
# ----------------
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True,
    handle_parsing_errors=True,
    agent_kwargs={
        "prefix": """

        You are a precise assistant. You MUST use tools for all data-related tasks.
        Never invent or guess information. Never rely on internal knowledge about vacations.

        TRAVEL RULE:
        For any question involving vacations, destinations, countries, flights, dates, or travel details:
            - You MUST call the appropriate tool: detect_country, list_countries, vacations_for_country, or summarize_vacation.
            - You MUST NOT answer from your own knowledge.
            - You MUST NOT create or infer vacation data.
            - You MUST NOT summarize SQL rows yourself. Use summarize_vacation.

        TOOL FORMAT RULE:
        When using a tool, follow EXACTLY this 3-line format:

        Thought: <your reasoning>
        Action: <tool name>
        Action Input: <input>

        Do NOT add anything before or after these three lines.
        Do NOT use parentheses after Action.
        Do NOT write Action: tool_name("input").
        Do NOT wrap Action Input with parentheses or quotes.

        If no tool is required, answer normally.

        """
    }
)

# # ⭐ Example Query:
# # ------------------
# result = agent.invoke({"input": "Find flights to greece."})
# print(result)

# function to export:
# --------------------
def ask_ai_agent(prompt_ai: str):
    clean_prompt = prompt_ai.strip()
    if len(clean_prompt) == 0:
        return "No prompt received."
    else:
        return agent.invoke({"input": clean_prompt})

print(ask_ai_agent("Please recommend a healthy morning routine for a 58-year-old male."))