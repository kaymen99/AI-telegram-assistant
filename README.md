# Telegram AI Agent

**Imagine a personal assistant in your pocket 📱 that handles your emails 📧, schedule 📅, and to-do lists ✅—all through Telegram. That's what this Telegram AI agent does! 🤖✨**

This project provides a personal assistant agent that manages tasks related to your email inbox, calendar, and Notion to-do list. The assistant communicates with you via Telegram, keeping you informed about your schedule, tasks, and emails. The assistant is equipped with sub-agents for handling specific tasks and tools for efficient task management.

<p align="center">
  <img src="https://github.com/user-attachments/assets/c38f1e65-05ca-4ed5-97da-283983348a63" alt="AI Telegram agent">
</p>

## Overview

### Main Agent: Telegram Assistant Manager

The Telegram Assistant Manager is your personal assistant that orchestrates the tasks and communication between you and the sub-agents. The manager is responsible for:

- Receiving and analyzing your Telegram messages.
- Delegating tasks to the appropriate sub-agent (Email, Calendar, or Notion).
- Communicating updates, messages, and any queries back to you via Telegram.

### Sub-Agents

The project includes three specialized sub-agents:

1. **Email Agent:** can handle all your email-related tasks, including sending emails, retrieving specific emails, and checking for important messages from your contacts list.

2. **Calendar Agent:** can manage your calendar by creating new events and retrieving and checking your scheduled events.

3. **Notion Agent:** can manage your to-do list in Notion, helping you add, remove, or check tasks as needed

All the sub-agents report back to the Telegram Assistant Manager after completing their respective tasks.

## Tech Stack

- **LangGraph & LangChain**: Frameworks used for building the AI agents and interacting with LLMs (GPT4, LLAMA3, GEMINI)
- **LangSmith**: For monitoring the different LLM calls and AI agents interactions.
- **Google APIs**: Provides access to Google services like Calendar, Contacts, and Gmail.
- **Notion Client**: Interface for interacting with Notion to manage and update to-do lists.

## How to Run

### Prerequisites

- Python 3.9+
- Google API credentials (for Calendar, Contacts, and Gmail access)
- Notion API key
- Groq API key (for Llama3)
- Google Gemini API key (for using the Gemini model)
- Create a Telegram Bot
- Necessary Python libraries (listed in `requirements.txt`)

### Setup

1. **Clone the repository:**

   ```sh
   git clone https://github.com/kaymen/AI-telegram-assistant.git
   cd AI-telegram-assistant
   ```

2. **Create and activate a virtual environment:**

   ```sh
   python -m venv venv
   source venv/bin/activate # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   Create a `.env` file in the root directory of the project and add your API keys, see `.env.example` to know all the parameters you will need.

5. **Configure Google API credentials:**

   Follow Google's documentation to set up credentials for Calendar, Contacts, and Gmail APIs. Save the credentials file in a secure location and update the path in the configuration file.

6. **Create a Telegram Bot:**

To interact with the assistant via Telegram, you will need to create a Telegram bot and obtain the bot token and chat ID. Follow this [guide](https://www.youtube.com/watch?v=ozQfKhdNjJU) to create your bot and get the necessary information.

7. **Run the project**:

   ```bash
   python main.py
   ```

### Usage

- **Communicating with the Assistant**: Simply send a message to your Telegram bot, and the assistant will analyze the message, delegate the task to the appropriate sub-agent, and report back with the results.

## Contribution

Feel free to fork the repository, create a branch, and submit a pull request if you'd like to contribute to the project.

## Contact

For any queries or suggestions, please reach out to [aymenMir1001@gmail.com](mailto:aymenMir1001@gmail.com).