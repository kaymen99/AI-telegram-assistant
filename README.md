<!--
Title: Telegram Assistant Agent | ReAct Agent
Description: Enhance your productivity with our Telegram AI Assistant, built using Langgraph ReAct. Manage emails, calendars, and Notion to-do lists seamlessly. Features include task delegation, email management, calendar scheduling, and Notion integration.
Keywords: Telegram bot, Langgraph ReAct, task automation, email management, calendar scheduling, Notion integration, AI assistant, productivity bot, Telegram API, Python bot development, AI agents
Author: kaymen99
-->

# Telegram AI Assistant Agent

**Imagine a personal assistant in your pocket 📱 that handles your emails 📧, schedule 📅, and to-do lists ✅—all through Telegram. That's what this Telegram AI agent does! 🤖✨**

This project provides a personal assistant agent that manages tasks related to your email inbox, calendar, and Notion to-do list. The assistant communicates with you via Telegram, keeping you informed about your schedule, tasks, and emails. The assistant is equipped with sub-agents for handling specific tasks and tools for efficient task management.

## Overview

### Main Assistant Agent: Telegram Assistant Manager

The Telegram Assistant Manager is your personal assistant that orchestrates the tasks and communication between you and the sub-agents. The manager is responsible for:

- Receiving and analyzing your Telegram messages.
- Delegating tasks to the appropriate sub-agent (Email, Calendar, or Notion).
- Communicating updates, messages, and any queries back to you via Telegram using a markdown format.

### Sub-Agents

The project includes three specialized sub-agents:

1. **Email Agent**
   - Manages your email inbox, including reading, writing, and sending emails.
   - Uses tools like FindContactEmail, ReadEmails, and SendEmail.

2. **Calendar Agent**
   - Manages your calendar, including checking availability, creating events, and retrieving scheduled events.
   - Uses tools like FindContactEmail, GetCalendarEvents, and CreateEvent.

3. **Notion Agent**
   - Manages your Notion to-do list, including retrieving tasks and adding new ones.
   - Uses tools like GetMyTodoList and AddTaskInTodoList.

All the sub-agents report back to the Telegram Assistant Manager after completing their respective tasks.

## Capabilities

- **Email Management**: The assistant can handle all your email-related tasks, including sending emails, retrieving specific emails, and checking for important messages.
- **Calendar Management**: The assistant can manage your calendar by creating, retrieving, and checking events, ensuring you're always on top of your schedule.
- **Notion Management**: The assistant can manage your to-do list in Notion, helping you add, remove, or check tasks as needed.

## Langgraph ReAct Agent

This project is built using the Langgraph ReAct agent, which combines reasoning and action to make intelligent decisions. The ReAct method enables the agents to think through a problem step by step and then take appropriate actions to achieve the desired outcome.

### Concept

The ReAct agent works by alternating between reasoning and actions. First, the agent reasons about the task at hand, breaking it down into smaller steps. Then, it selects the best action to take at each step, ensuring that the overall goal is achieved efficiently. This method allows the agents to handle complex tasks by thinking critically and executing actions in a structured manner.

### Example

Imagine you ask the Telegram Assistant to "Check if I have any meetings today and email Emily if I'm available for a meeting at 3 PM." Here's how the ReAct agent would handle this:

1. **Reasoning**: The agent first identifies two tasks: checking the calendar and sending an email.
2. **Action**: The agent delegates the calendar task to the Calendar Agent to retrieve today's meetings.
3. **Reasoning**: After receiving the meeting details, the agent checks if you're available at 3 PM.
4. **Action**: If available, the agent delegates the email task to the Email Agent to send the message to Emily.

This approach ensures that the agent handles the request accurately, considering each step's outcome before proceeding.

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

# AI-telegram-assistant
