from typing import Optional, Type
from langchain_core.callbacks import CallbackManagerForToolRun
from langsmith import traceable
from pydantic import BaseModel, Field
from langchain.tools import BaseTool

from src.agents.email_agent import invoke_email_agent
from src.agents.calendar_agent import invoke_calendar_agent
from src.agents.notion_agent import invoke_notion_agent


class DelegateInput(BaseModel):
    agent_name: str = Field(description="Name of the subagent to delegate to")
    task: str = Field(description="Task to delegate to the subagent")

class Delegate(BaseTool):
    name: str = "Delegate"
    description: str = "Use this to delegate a task to one of your subagents"
    args_schema: Type[BaseModel] = DelegateInput
    
    def delegate(self, agent_name: str, task: str) -> str:
        """
        Simulates delegating a task to a subagent
        """
        print(f"Task '{task}' has been delegated to the {agent_name} agent.")
        if agent_name == "Email Agent":
            return invoke_email_agent(task)
        elif agent_name == "Calendar Agent":
            return invoke_calendar_agent(task)
        elif agent_name == "Notion Agent":
            return invoke_notion_agent(task)
        else:
            return "Invalid agent name"

    @traceable(run_type="tool", name="Delegate")
    def _run(
        self,
        agent_name: str,
        task: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        return self.delegate(agent_name, task)