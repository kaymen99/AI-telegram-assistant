import os
from datetime import datetime, timezone
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

class GetCalendarEventsInput(BaseModel):
    start_date: str = Field(description="Start date for fetching events")
    end_date: str = Field(description="End date for fetching events")

class GetCalendarEvents(BaseTool):
    name = "GetCalendarEvents"
    description = "Use this to retrieve all calendar events between 2 date periods from my calendar"
    args_schema: Type[BaseModel] = GetCalendarEventsInput

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

    def get_calendar_events(self, start_time, end_time):
        """
        Fetches calendar events from Google Calendar
        """
        try:
            creds = self.get_credentials()
            service = build("calendar", "v3", credentials=creds)

            # Convert string times to datetime objects and ensure they're in UTC
            start_datetime = datetime.fromisoformat(start_time).replace(tzinfo=timezone.utc)
            end_datetime = datetime.fromisoformat(end_time).replace(tzinfo=timezone.utc)

            # Format date-times in RFC3339 format
            start_rfc3339 = start_datetime.isoformat().replace('+00:00', 'Z')
            end_rfc3339 = end_datetime.isoformat().replace('+00:00', 'Z')

            events = service.events().list(
                calendarId='primary',
                timeMin=start_rfc3339,
                timeMax=end_rfc3339,
                singleEvents=True,
                orderBy='startTime'
            ).execute()

            if not events:
                return "No events found in the specified time range."

            event_list = []
            for event in events['items']:
                start = event['start'].get('dateTime', event['start'].get('date'))
                event_list.append(f"Event: {event['summary']}, Description: {event['description']}, Start: {start}")
            
            if event_list:
                return "\n".join(event_list)
            return "No event found for this dates"

        except HttpError as error:
            return f"An error occurred: {error}"

    @traceable(run_type="tool", name="GetCalendarEvents")
    def _run(
        self,
        start_date: str,
        end_date: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        return self.get_calendar_events(start_date, end_date)