import os
from dotenv import load_dotenv
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

load_dotenv()

DATABASE_AGENT_URL = os.getenv("DATABASE_AGENT_URL")
PATH_TO_YOUR_MCP_SERVER_SCRIPT = r"C:\Users\mm0954\Documents\maventic_ai_101\mcp_server\adk_mcp_server.py"

remote_agent = RemoteA2aAgent(
    name="database_orchestrator",
    description=(
        "Database agent is an AI agent capable of db operations on the server. It can perform insertions, deletions, updations and retrival from that database."
    ),
    agent_card=f"{DATABASE_AGENT_URL}{AGENT_CARD_WELL_KNOWN_PATH}",
)

web_reader_mcp_client_agent = LlmAgent(
    model=LiteLlm(model="groq/openai/gpt-oss-20b"),
    name='web_reader_mcp_client_agent',
    instruction="Use the 'load_web_page' tool to fetch content from a URL provided by the user.",
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command='uv',
                    args=['run', PATH_TO_YOUR_MCP_SERVER_SCRIPT],
                )
            )
        )
    ],
)


root_agent = Agent(
    model=LiteLlm(model="groq/openai/gpt-oss-20b"),
    name='Orchestrator_Agent',
    description="""You are "Maventic" the Orchestrator agent.""",
    instruction='Answer user questions to the best of your knowledge, use the tools and sub agents to perform tasks based on the user requirements.',
    sub_agents=[remote_agent, web_reader_mcp_client_agent],
)
