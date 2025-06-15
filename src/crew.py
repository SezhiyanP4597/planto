import os
import yaml
from dotenv import load_dotenv
from crewai import Task, Crew, Process
from crewai_tools import ScrapeWebsiteTool
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Custom Gemini 1.5 Flash wrapper
class GeminiFlashAgent:
    def __init__(self, role, goal, backstory, tools=None, verbose=False):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.tools = tools or []
        self.verbose = verbose
        self.model = genai.GenerativeModel("models/gemini-1.5-flash")

    def run(self, task_description):
        # Optional: Run tools first (like scraper)
        context = ""
        for tool in self.tools:
            context += f"\n[Tool Output]\n{tool.run(task_description)}\n"

        prompt = f"""
You are a helpful agent with the following role: {self.role}

Goal: {self.goal}
Backstory: {self.backstory}

[User Task]
{task_description}

{context}
Please respond as clearly and helpfully as possible based only on the website context.
"""
        if self.verbose:
            print("\n=== PROMPT ===\n", prompt)

        response = self.model.generate_content(prompt)
        return response.text

# Load configs
with open("src/config/agents.yaml", "r") as f:
    agents_config = yaml.safe_load(f)

with open("src/config/tasks.yaml", "r") as f:
    tasks_config = yaml.safe_load(f)

# Setup tool
scraper = ScrapeWebsiteTool(website_url="https://planto.ai/")

# Agent config
agent_data = agents_config["planto_chat_agent"]
chat_agent = GeminiFlashAgent(
    role=agent_data["role"],
    goal=agent_data["goal"],
    backstory=agent_data["backstory"],
    tools=[scraper],
    verbose=True,
)

# Function to dynamically create and run task
def create_crew_for_question(user_input: str):
    task_data = tasks_config["chat_task"]
    task_description = task_data["description"].format(user_input=user_input)

    response = chat_agent.run(task_description)
    return response
