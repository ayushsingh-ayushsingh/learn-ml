from google.adk.a2a.utils.agent_to_a2a import to_a2a
from dotenv import load_dotenv
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

load_dotenv()

remote_agent = RemoteA2aAgent(
    name="database_orchestrator",
    description=(
        "Database agent is an AI agent capable of db operations on the server. It can perform insertions, deletions, updations and retrival from that database."
    ),
    agent_card=f"http://localhost:8001/{AGENT_CARD_WELL_KNOWN_PATH}",
)

root_agent = Agent(
    model=LiteLlm(model="groq/openai/gpt-oss-20b"),
    name='Orchestrator_Agent',
    description="""You are "Maventic" the Orchestrator agent.""",
    instruction='Answer user questions to the best of your knowledge, use the tools and sub agents to perform tasks based on the user requirements.',
    sub_agents=[remote_agent],
)
