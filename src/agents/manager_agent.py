from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from src.tools.delegate_tool import Delegate
from src.tools.telegram import SendTelegram
from src.prompts import TELEGRAM_ASSISTANT_MANAGER_PROMPT
from src.utils import print_stream
from dotenv import load_dotenv

# Load .env variables
load_dotenv()


# Initialize the AI model (ChatGroq with llama3 model)
# model = ChatGroq(model="llama-3.1-70b-versatile")
# model = ChatGroq(model="llama3-70b-8192")

# Uncomment and use the following line if you want to use the Gemini model from Google Generative AI
model = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

# Initialize the tools
tools = [SendTelegram(), Delegate()]

# Initialize memory saver for the agent
memory = MemorySaver()

# Create the react agent with the specified LLM, tools, agent prompt, and memory
manager_agent = create_react_agent(model, tools, state_modifier=TELEGRAM_ASSISTANT_MANAGER_PROMPT, checkpointer=memory)

# Configuration for the agent (e.g., specifying thread ID)
config = {"configurable": {"thread_id": "manager-thread"}, "recursion_limit": 1000}


def invoke_telegram_assistant(message):
    inputs = {"messages": [("user", message)]}
    print_stream(manager_agent.stream(inputs, config=config, stream_mode="values"))