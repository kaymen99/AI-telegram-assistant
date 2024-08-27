from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langsmith import traceable
from src.tools.email import SendEmail, FindContactEmail
from src.prompts import EMAIL_AGENT_PROMPT
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
tools = [SendEmail(), FindContactEmail()]

# Initialize memory saver for the agent
memory = MemorySaver()

# Create the react agent with the specified LLM, tools, agent prompt, and memory
email_agent = create_react_agent(model, tools, state_modifier=EMAIL_AGENT_PROMPT, checkpointer=memory)

# Configuration for the agent (e.g., specifying thread ID)
email_config = {"configurable": {"thread_id": "email-thread"}}


@traceable(run_type="llm", name="Email Agent")
def invoke_email_agent(task: str) -> str:
    inputs = {"messages": [("user", task)]}
    print_stream(email_agent.stream(inputs, config=email_config, stream_mode="values"))
    return email_agent.get_state(config=email_config).values["messages"][-1].content