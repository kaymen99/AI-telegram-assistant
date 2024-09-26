from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langsmith import traceable
from src.tools.notion import GetMyTodoList, AddTaskInTodoList
from src.prompts import NOTION_AGENT_PROMPT
from src.utils import print_agent_output
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Initialize LLM model
# model = ChatGroq(model="llama-3.1-70b-versatile")
# model = ChatGroq(model="llama3-70b-8192")
model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.1)

# Initialize the tools
tools = [GetMyTodoList(), AddTaskInTodoList()]

# Create the react agent with the specified LLM, tools, system prompt
notion_agent = create_react_agent(model, tools, state_modifier=NOTION_AGENT_PROMPT)


@traceable(run_type="llm", name="Notion Agent")
def invoke_notion_agent(task: str) -> str:
    inputs = {"messages": [("user", task)]}
    output = notion_agent.invoke(inputs)
    print_agent_output(output)
    return output["messages"][-1].content