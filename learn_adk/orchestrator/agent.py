import os
from dotenv import load_dotenv
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams, StreamableHTTPConnectionParams
from mcp import StdioServerParameters

load_dotenv()

DATABASE_AGENT_URL = os.getenv("DATABASE_AGENT_URL")
CHART_AGENT_URL = os.getenv("CHART_AGENT_URL")
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL")
PATH_OF_MCP_SERVER_SCRIPT = os.getenv("PATH_OF_MCP_SERVER_SCRIPT")

remote_agent = RemoteA2aAgent(
    name="database_orchestrator",
    description=(
        "Database agent is an AI agent capable of db operations on the server. It can perform insertions, deletions, updations and retrival from that database."
    ),
    agent_card=f"{DATABASE_AGENT_URL}{AGENT_CARD_WELL_KNOWN_PATH}",
)

remote_chart_agent = RemoteA2aAgent(
    name="chart_agent",
    description=(
        "Sales Chart Agent is an AI agent capable of generating "
        "monthly revenue charts using provided sales data."
    ),
    agent_card=f"{CHART_AGENT_URL}{AGENT_CARD_WELL_KNOWN_PATH}",
)

web_reader_mcp_client_agent = LlmAgent(
    model=LiteLlm(model="groq/openai/gpt-oss-20b"),
    name='web_reader_mcp_client_agent',
    instruction="Use the 'load_web_page' tool to fetch content from a URL or scrape a website URL provided by the user.",
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command='uv',
                    args=[
                        "run",
                        PATH_OF_MCP_SERVER_SCRIPT
                    ]
                )
            )
        )
    ],
)

file_creation_mcp_agent = LlmAgent(
    model=LiteLlm(model="groq/openai/gpt-oss-20b"),
    name='file_creation_mcp_agent',
    instruction="Use the 'create_file' tool to create file and add content to that file. If users says to save to desktop then use this desktop path: C:/Users/mm0954/Desktop if not specified save it without this."
    "If desktop specified to, say, create a hello.md file then C:/Users/mm0954/Desktop/hello.md and content = '# Hello, World!'"
    "Else if not specified then path should be hello.md and content = '# Hello, World!'"
    "If another path is specified by the user then use that path to save the file.",
    tools=[
        McpToolset(connection_params=StreamableHTTPConnectionParams(
            url=MCP_SERVER_URL,
        ))
    ],
)

root_agent = Agent(
    model=LiteLlm(model="groq/openai/gpt-oss-20b"),
    name='Orchestrator_Agent',
    description="""You are "Maventic" the Orchestrator agent.""",
    instruction='Answer user questions to the best of your knowledge, use the tools and sub agents to perform tasks based on the user requirements.',
    sub_agents=[remote_agent, web_reader_mcp_client_agent,
                remote_chart_agent, file_creation_mcp_agent],
)
