import os
import smtplib
from typing import Optional, Type
from langchain_core.callbacks import CallbackManagerForToolRun
from langsmith import traceable
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

os.environ["GMAIL_MAIL"] = "a.kerrour0909@gmail.com"
os.environ["GMAIL_APP_PASSWORD"] = "nrjp wbqk ktfr mmvx"

class SendEmailInput(BaseModel):
    to: str = Field(description="Email of the recipient")
    subject: str = Field(description="Subject of the email")
    body: str = Field(description="Body of the email")

class SendEmail(BaseTool):
    name: str = "SendEmail"
    description: str = "Use this to send emails to my contacts on my behalf"
    args_schema: Type[BaseModel] = SendEmailInput

    def send_email_with_gmail(self, email_recipient, email_subject, email_body):
        """
        Sends an email using Gmail SMTP
        """
        try:
            sender_email = os.getenv("GMAIL_MAIL")
            app_password = os.getenv("GMAIL_APP_PASSWORD")

            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = email_recipient
            msg['Subject'] = email_subject
            msg.attach(MIMEText(email_body, 'plain'))
            print(msg)

            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(sender_email, app_password)
            text = msg.as_string()
            server.sendmail(sender_email, email_recipient, text)
            server.quit()
            return "Email sent successfully."
        except Exception as e:
            return f"Email was not sent successfully, error: {e}"

    @traceable(run_type="tool", name="SendEmail")
    def _run(
        self,
        to: str,
        subject: str,
        body: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        return self.send_email_with_gmail(to, subject, body)