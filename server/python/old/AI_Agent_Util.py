from langchain_ollama import OllamaLLM
from langchain_classic.agents import initialize_agent, Tool
import re
from sql_util import run_query_sql, convert_recordset_to_dict
# https://chatgpt.com/c/69206897-d7fc-832b-be9d-ae571539cd6a

llm = OllamaLLM(model="mistral")
country_llm = OllamaLLM(model="mistral", temperature=0)


def Summarize_Vacation_Info(txt:str):    
    prompt = f"""
        Extract the COUNTRY mentioned in this user text.
        Return ONLY the country name, nothing else.
        If multiple countries appear, return the most relevant one.

        User text: {txt}

        Country:
    """
    result = country_llm.invoke(prompt)
    wanted_country = result.strip()
    wanted_country = wanted_country.replace(".", "").strip()
    # return wanted_country
    VALID_COUNTRIES = run_query_sql("SELECT DISTINCT destination FROM Vacations", "fetch")
    countries = [row[0] for row in VALID_COUNTRIES]
    if wanted_country in countries:
        # return wanted_country
        # now look for vacations to this country
        vacations = run_query_sql(f"SELECT * FROM Vacations WHERE destination LIKE '{wanted_country}%' ORDER BY startDate", "fetch")
        return [row[0] for row in vacations]
    else:
        return f"Unknown or invalid country: {wanted_country}"



# def sum_nums(txt:str):
#     nums = re.findall(r'\d+', txt) # there regex pattern (in raw string "r") means: get all appearances of digits (\d), but let me have them all (+).
#     # print(nums)
#     if len(nums) < 2:
#         return "Error: Please provide two numbers."
#     return int(nums[0]) + int(nums[1])

# # def mul_nums(num1: int, num2: int):
# #     return num1 * num2
# def mul_nums(txt:str):
#     nums = re.findall(r'\d+', txt)
#     # print(nums)
#     if len(nums) < 2:
#         return "Error: Please provide two numbers."
#     return int(nums[0]) * int(nums[1])

# def power_nums(txt:str):
#     nums = re.findall(r'\d+', txt)
#     if len(nums) < 2:
#         return "Error: Please provide two numbers."
#     return int(nums[0]) ** int(nums[1])

# def root_nums(txt:str):
#     nums = re.findall(r'\d+', txt)
#     if len(nums) < 2:
#         return "Error: Please provide two numbers."
#     if int(nums[1]) == 0:
#         return "Error: cannot calculate the 0th root."
#     # return int(nums[0]) ** (1 / int(nums[1])) #first version. Newer is:
#     base = int(nums[0])
#     n = int(nums[1])
#     result = base ** (1 / n)
#     # If result is extremely close to an integer, snap it to int
#     if abs(result - round(result)) < 1e-9:
#         return round(result)
#     return result

# tools = [
#     Tool(
#         name="Sum_Numbers",
#         func=sum_nums,
#         description="Add two integers ,input should be like : 'num1, num2'"
#     ),
#     Tool(
#         name="Multiply_Numbers",
#         func=mul_nums,
#         description="Multiply two integers: 'num1, num2'"
#     ),
#     Tool(
#         name="Power_Numbers",
#         func=power_nums,
#         description="Calculate Power of two integers: 'num1, num2'"
#     ),
#     Tool(
#         name="Root_Numbers",
#         func=root_nums,
#         description="Calculate Root of two integers: 'num1, num2'"
#     )
# ]

tools = [
    Tool(
        name="detect_country",
        func=Summarize_Vacation_Info,
        description="Extract the country name from any travel-related free text."
    )    
]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True,
    handle_parsing_errors=True,
    agent_kwargs={
        "prefix": """You are a helpful assistant.
        Use tools ONLY when needed.

        When using a tool, follow THIS EXACT format:

        Thought: <your reasoning>
        Action: <tool name>
        Action Input: <input to the tool>

        Never use parentheses after Action.
        Never write ToolName('input').
        Never write Action: ToolName("input").
        Never wrap inputs in parentheses.

        Answer normally if no tool is required.
        """
    }
)

# Alternative (easier!!) fix
# Use names without capitals and very short:
# sum_numbers
# multiply
# power
# root
# LLMs behave better with simple names:
# tools = [
#     Tool(name="sum", func=sum_nums, description="Sum numbers"),
#     Tool(name="mul", func=mul_nums, description="Multiply numbers"),
#     Tool(name="pow", func=power_nums, description="Power a^b"),
#     Tool(name="root", func=root_nums, description="Nth root")
# ]

# BEST fix (recommended): Enable error recovery
# agent = initialize_agent(
#     tools=tools,
#     llm=llm,
#     agent="zero-shot-react-description",
#     verbose=True,
#     handle_parsing_errors=True
# )

# result = agent.invoke({"input": "What is the sum of 15 and 25, then multiply the result by 2?"})
# result = agent.invoke({"input": "How much is 4 to the power of 5?"}) #should give 1024
# result = agent.invoke({"input": "What is the 5th root of 1024?"}) #should give 4
# print(result)

# result = agent.invoke({"input": "Find flights to Greece."})
result = agent.invoke({"input": "Find flights to greece."})
print(result)