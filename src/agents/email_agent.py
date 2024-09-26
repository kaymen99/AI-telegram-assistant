from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langsmith import traceable
from src.tools.email import SendEmail, FindContactEmail, ReadEmails
from src.prompts import EMAIL_AGENT_PROMPT
from src.utils import print_agent_output
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Initialize LLM model
# model = ChatGroq(model="llama-3.1-70b-versatile")
# model = ChatGroq(model="llama3-70b-8192")
model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.1)

# Initialize the tools
tools = [SendEmail(), FindContactEmail(), ReadEmails()]

# Create the react agent with the specified LLM, tools, system prompt
email_agent = create_react_agent(model, tools, state_modifier=EMAIL_AGENT_PROMPT)


@traceable(run_type="llm", name="Email Agent")
def invoke_email_agent(task: str) -> str:
    inputs = {"messages": [("user", task)]}
    output = email_agent.invoke(inputs)
    print_agent_output(output)
    return output["messages"][-1].content