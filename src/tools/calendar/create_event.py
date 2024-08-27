import os
from datetime import datetime, timedelta
from typing import Optional, Type
from langchain_core.callbacks import CallbackManagerForToolRun
from langsmith import traceable
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

from src.utils import SCOPES

class CreateEventInput(BaseModel):
    title: str = Field(description="Title of the event")
    description: str = Field(description="Description of the event")
    start_time: str = Field(description="Start time of the event")

class CreateEvent(BaseTool):
    name = "CreateEvent"
    description = "Use this to create a new event in my calendar"
    args_schema: Type[BaseModel] = CreateEventInput

    def get_credentials(self):
        """
        Get and refresh Google Calendar API credentials
        """
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        return creds

    def create_event(self, title, desc, start):
        """
        Creates an event on Google Calendar
        """
        try:
            creds = self.get_credentials()
            service = build("calendar", "v3", credentials=creds)

            # Convert the string to a datetime object
            event_datetime = datetime.fromisoformat(start)

            event = {
                'summary': title,
                'description': desc,
                'start': {
                    'dateTime': event_datetime.isoformat(),
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': (event_datetime + timedelta(hours=1)).isoformat(),
                    'timeZone': 'UTC',
                },
            }

            event = service.events().insert(calendarId='primary', body=event).execute()
            return f"Event created successfully. Event ID: {event.get('id')}"

        except HttpError as error:
            return f"An error occurred: {error}"

    @traceable(run_type="tool", name="CreateEvent")
    def _run(
        self,
        title: str,
        description: str,
        start_time: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        return self.create_event(title, description, start_time)