import os, requests
from datetime import datetime
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

class GetMyTodoListInput(BaseModel):
    date: str = Field(description="Date for which to retrieve tasks (YYYY-MM-DD)")

class GetMyTodoList(BaseTool):
    name = "GetMyTodoList"
    description = "Use this to retrieve tasks from your Notion to-do list for a specific date"
    args_schema: Type[BaseModel] = GetMyTodoListInput

    def get_tasks_for_date(self, target_date):
        try:
            # Parse the target date string into a datetime object
            try:
                target_datetime = datetime.strptime(target_date, "%Y-%m-%d")
            except ValueError:
                print(f"Error: Invalid date format. Please use YYYY-MM-DD format.")
                return []

            # Set up the filter to get tasks due on the target date
            filter_params = {
                "filter": {
                    "property": "Date",
                    "date": {
                        "equals": target_date
                    }
                }
            }

            results = notion.databases.query(database_id=database_id, **filter_params)
            tasks = []

            for page in results["results"]:
                due_date = page["properties"]["Date"]["date"]["start"]

                # Parse the due date from Notion
                due_datetime = datetime.fromisoformat(due_date.replace("Z", "+00:00"))

                # Check if the task is due on the target date
                if due_datetime.date() == target_datetime.date():
                    task = {
                        "id": page["id"],
                        "title": page["properties"]["Title"]["title"][0]["text"]["content"],
                        "status": page["properties"]["Status"]["status"]["name"],
                        "due_date": due_date
                    }
                    tasks.append(task)

            if tasks:
                return f"Todo list for {target_datetime}:\n" + "\n".join([str(task) for task in tasks])
            else:
                return f"No tasks found in Todo list for {target_datetime}."

        except Exception as e:
            return f"An error occurred: {str(e)}"

    @traceable(run_type="tool", name="GetMyTodoList")
    def _run(
        self,
        date: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        return self.get_tasks_for_date(date)