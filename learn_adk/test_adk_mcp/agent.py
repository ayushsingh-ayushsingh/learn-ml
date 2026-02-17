from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

PATH_TO_YOUR_MCP_SERVER_SCRIPT = r"C:\Users\mm0954\Documents\maventic_ai_101\mcp_server\adk_mcp_server.py"

if PATH_TO_YOUR_MCP_SERVER_SCRIPT == r"C:\Users\mm0954\Documents\maventic_ai_101\mcp_server\adk_mcp_server.py":
    print("WARNING: PATH_TO_YOUR_MCP_SERVER_SCRIPT is not set. Please update it in agent.py.")

root_agent = LlmAgent(
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
