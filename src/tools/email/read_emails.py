import os
from typing import Optional, Type
from langchain_core.callbacks import CallbackManagerForToolRun
from langsmith import traceable
from pydantic import BaseModel, Field
from typing import Optional, Type
from langchain.tools import BaseTool
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from email.utils import parsedate_to_datetime

from src.utils import SCOPES

class ReadEmailsInput(BaseModel):
    from_date: str = Field(description="From date for reading emails in format: YYYY/MM/DD")
    to_date: str = Field(description="To date for reading emails in format: YYYY/MM/DD")
    email: Optional[str] = Field(description="Email of the contact to read emails from")

class ReadEmails(BaseTool):
    name: str = "ReadEmails"
    description: str = "Use this to retrieve emails from my inbox"
    args_schema: Type[BaseModel] = ReadEmailsInput

    def get_credentials(self):
        """
        Get and refresh Gmail API credentials
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

    def fetch_emails(self, from_date, to_date, email=""):
        """
        Fetches emails from Gmail inbox
        """
        try:
            creds = self.get_credentials()
            service = build('gmail', 'v1', credentials=creds)

            from_date = datetime.fromisoformat(from_date.replace('/', '-')).replace(tzinfo=timezone.utc)
            to_date = datetime.fromisoformat(to_date.replace('/', '-')).replace(tzinfo=timezone.utc)

            query = f'after:{from_date.strftime("%Y/%m/%d")} before:{to_date.strftime("%Y/%m/%d")}'
            if email:
                query += f' from:{email}'

            results = service.users().messages().list(userId='me', q=query).execute()
            messages = results.get('messages', [])

            if not messages:
                return "No emails found in the specified time range."

            email_list = []
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()

                subject = next((header['value'] for header in msg['payload']['headers'] if header['name'] == 'Subject'), 'No Subject')
                from_email = next((header['value'] for header in msg['payload']['headers'] if header['name'] == 'From'), 'Unknown Sender')
                date = next((header['value'] for header in msg['payload']['headers'] if header['name'] == 'Date'), '')
                date_obj = parsedate_to_datetime(date)
                if date_obj.tzinfo is None:
                    date_obj = date_obj.replace(tzinfo=timezone.utc)

                if from_date <= date_obj <= to_date:
                    snippet = msg['snippet']
                    email_list.append(f"From: {from_email}\nSubject: {subject}\nDate: {date}\nSnippet: {snippet}\n")

            return "\n".join(email_list)

        except HttpError as error:
            return f"An error occurred: {error}"

    @traceable(run_type="tool", name="ReadEmails")
    def _run(
        self,
        from_date: str,
        to_date: str,
        email: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        return self.fetch_emails(from_date, to_date, email)