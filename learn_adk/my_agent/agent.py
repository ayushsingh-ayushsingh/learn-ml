from google.adk.a2a.utils.agent_to_a2a import to_a2a
from dotenv import load_dotenv
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from .db_functions import db_tools

load_dotenv()

database_agent = Agent(
    name='Database_Agent',
    model=LiteLlm(model="groq/openai/gpt-oss-20b"),
    description='Database agent is an AI agent capable of db operations on the server. It can perform insertions, deletions, updations and retrival from that database.',
    instruction='Answer user questions to the best of your knowledge, use relavant tools that perform SQL queries in the database. You are a Database agent capable of db operations on the server. It can perform insertions, deletions, updations and retrival from that database.',
    tools=db_tools,
)

root_agent = Agent(
    model=LiteLlm(model="groq/openai/gpt-oss-20b"),
    name='Orchestrator_Agent',
    description="""You are "Maventic" the Orchestrator agent.""",
    instruction='Answer user questions to the best of your knowledge, use the tools and sub agents to perform tasks based on the user requirements.',
    sub_agents=[database_agent]
)

a2a_app = to_a2a(root_agent, port=8001)
