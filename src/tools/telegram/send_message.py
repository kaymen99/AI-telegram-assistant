import os, requests
from typing import Optional, Type
from langchain_core.callbacks import CallbackManagerForToolRun
from langsmith import traceable
from pydantic import BaseModel, Field
from langchain.tools import BaseTool

class SendTelegramInput(BaseModel):
    message: str = Field(description="Message to send")

class SendTelegram(BaseTool):
    name = "SendTelegram"
    description = "Use this to send a message to my telegram account"
    args_schema: Type[BaseModel] = SendTelegramInput

    def send_message(self, text):
        TOKEN = os.getenv("TELEGRAM_TOKEN")
        CHAT_ID = os.getenv("CHAT_ID")

        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}&amp;parse_mode=MarkdownV2"
        response = requests.get(url).json()
        if not response["ok"]:
            return "Failed to send message"

        return "Message sent successfully on Telegram"

    @traceable(run_type="tool", name="SendTelegram")
    def _run(
        self,
        message: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        return self.send_message(message)
