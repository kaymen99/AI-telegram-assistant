import os
from enum import Enum
from typing import Optional, Type
from langchain_core.callbacks import CallbackManagerForToolRun
from langsmith import traceable
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from notion_client import Client

# Initialize the Notion client
notion = Client(auth=os.getenv("NOTION_TOKEN"))

# Your database ID
database_id = os.getenv("NOTION_DATABASE_ID")

class TaskStatus(Enum):
    NOT_STARTED = "Not started"
    IN_PROGRESS = "In progress"
    COMPLETED = "Done"

class AddTaskInTodoListInput(BaseModel):
    task: str = Field(description="Task to be added")
    date: str = Field(description="Date and time for the task (YYYY-MM-DD) (HH:MM)")

class AddTaskInTodoList(BaseTool):
    name = "AddTaskInTodoList"
    description = "Use this to add a new task to your Notion to-do list"
    args_schema: Type[BaseModel] = AddTaskInTodoListInput

    def add_task(self, task, due_date=None):
        try:
            new_task = {
                "Title": {"title": [{"text": {"content": task}}]},
                "Status": {"status": {"name": TaskStatus.NOT_STARTED.value}},
            }
            if due_date:
                new_task["Date"] = {"date": {"start": due_date}}

            notion.pages.create(parent={"database_id": database_id}, properties=new_task)

            return f"Task '{task}' added successfully to Todo list for {due_date}."
        except Exception as e:
            return f"An error occurred: {str(e)}"

    @traceable(run_type="tool", name="AddTaskInTodoList")
    def _run(
        self,
        task: str,
        date: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        return self.add_task(task, date)