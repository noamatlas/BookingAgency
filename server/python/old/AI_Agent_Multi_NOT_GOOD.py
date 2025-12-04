# ------------------------------------------------------------
# Imports
# ------------------------------------------------------------
from langchain_ollama import OllamaLLM
from langchain_classic.agents import initialize_agent, Tool
from langchain_classic.memory import ConversationBufferMemory
import re
import pyodbc
from sql_util import run_query_sql


# ------------------------------------------------------------
# Two LLMs
# ------------------------------------------------------------

# ⚙️ Deterministic LLM for agent + tools
llm_tools = OllamaLLM(model="mistral", temperature=0)

# 💬 Creative LLM for general chat
llm_free_chat = OllamaLLM(model="mistral", temperature=0.8)


# ------------------------------------------------------------
# TOOL 1: Intent detection (is the question travel-related?)
# ------------------------------------------------------------
def detect_intent(text: str):
    prompt = f"""
    Decide whether this user message is about TRAVEL/VACATIONS
    or GENERAL CHAT. Return exactly one word:

    - "travel"
    - "general"

    Message: {text}
    Decision:
    """
    result = llm_tools.invoke(prompt).strip().lower()

    if "travel" in result:
        return "travel"
    return "general"


# ------------------------------------------------------------
# TOOL 2: Detect country (LLM-only)
# ------------------------------------------------------------
def detect_country(text: str):
    prompt = f"""
    Extract the COUNTRY mentioned in this text.
    Return only the country name. Nothing else.

    If multiple appear, return the most relevant one.

    Text: {text}

    Country:
    """
    result = llm_tools.invoke(prompt)
    return result.strip().replace(".", "").strip()


# ------------------------------------------------------------
# TOOL 3: List valid countries (SQL-only)
# ------------------------------------------------------------
def list_countries(_):
    rows = run_query_sql("SELECT DISTINCT destination FROM Vacations", "fetch")
    return [row[0] for row in rows]


# ------------------------------------------------------------
# TOOL 4: Fetch vacations for a given country (SQL-only)
# ------------------------------------------------------------
def vacations_for_country(country: str):
    country = country.strip().replace("'", "''")
    rows = run_query_sql(
        f"""
        SELECT id, title, destination, startDate, endDate, price,
               fullDescription, availablePlaces, imagesPaths, agentId,
               createdAt, updatedAt
        FROM Vacations
        WHERE destination LIKE '{country}%'
        ORDER BY startDate
        """,
        "fetch",
    )
    return rows


# ------------------------------------------------------------
# TOOL 5: Summarize a vacation record (LLM-only)
# ------------------------------------------------------------
def summarize_vacation(record: str):
    prompt = f"""
    Convert this raw SQL vacation record into a friendly explanation.

    Record:
    {record}

    Summary:
    """
    return llm_tools.invoke(prompt).strip()


# ------------------------------------------------------------
# Register tools
# ------------------------------------------------------------
tools = [
    Tool(name="detect_intent", func=detect_intent,
         description="Decide if user query is about travel or general chat."),
    Tool(name="detect_country", func=detect_country,
         description="Extract a country name from user text."),
    Tool(name="list_countries", func=list_countries,
         description="List all valid vacation destinations."),
    Tool(name="vacations_for_country", func=vacations_for_country,
         description="Get vacation records for a given country."),
    Tool(name="summarize_vacation", func=summarize_vacation,
         description="Convert a vacation SQL row into readable text.")
]


# ------------------------------------------------------------
# Memory
# ------------------------------------------------------------
memory = ConversationBufferMemory(memory_key="chat_history")


# ------------------------------------------------------------
# AGENT (deterministic LLM)
# ------------------------------------------------------------
agent = initialize_agent(
    tools=tools,
    llm=llm_tools,
    agent="zero-shot-react-description",
    verbose=True,
    handle_parsing_errors=True,
    memory=memory,
    agent_kwargs={
        "prefix": """
You are a precise assistant.

INTENT RULE:
Always begin by using detect_intent to decide whether the question is TRAVEL or GENERAL.
If the result is "general", DO NOT TRY TO USE TRAVEL TOOLS. Instead, return: "__general__".

TRAVEL RULE:
If intent is "travel":
    - You MUST use detect_country, list_countries, vacations_for_country.
    - You must NOT create or guess travel data.
    - You must NOT summarize vacation rows yourself: use summarize_vacation tool.
    - Never invent information.

TOOL FORMAT RULE:
When using a tool, follow EXACTLY this format:

Thought: <reasoning>
Action: <tool name>
Action Input: <input>

Do NOT add anything before/after these three lines.
Do NOT use parentheses after Action.
Do NOT write Action: tool_name("input").
Do NOT wrap Action Input in quotes unless the input contains spaces.
"""
    }
)


# ------------------------------------------------------------
# DISPATCHER: High-level wrapper
# ------------------------------------------------------------
def assistant_message(user_input):
    """
    This function routes:
        - travel questions → agent_with_tools
        - general chat → free LLM
    """

    # First: ask the agent to detect intent
    intent = agent.invoke({"input": f"detect intent: {user_input}"})

    if isinstance(intent, dict):
        intent = intent.get("output", "")

    if "__general__" in intent or "general" in intent.lower():
        # Use creative LLM
        return llm_free_chat.invoke(user_input)

    # Travel → use full agent
    result = agent.invoke({"input": user_input})
    return result["output"] if isinstance(result, dict) else result


# ------------------------------------------------------------
# EXAMPLE USAGE
# ------------------------------------------------------------
print(assistant_message("Find flights to greece."))
print("----------------------------------------------------")
print(assistant_message("Please recommend a healthy morning routine for a 58-year-old male."))
