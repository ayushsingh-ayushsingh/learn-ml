from dotenv import load_dotenv
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from .chart_tools import generate_sales_chart

load_dotenv()

root_agent = Agent(
    name="Chart_Agent",
    model=LiteLlm(model="groq/openai/gpt-oss-20b"),
    description=(
        "Sales Chart Agent is an AI agent capable of generating "
        "monthly revenue charts using provided sales data."
    ),
    instruction=(
        "You are a Sales Chart Agent. "
        "If the user provides monthly sales data, "
        "extract the month and revenue values correctly "
        "and use the generate_sales_chart tool to create the chart. "
        "Ensure the data format is a list of tuples like "
        "[('Jan', 1000), ('Feb', 1500)]."
    ),
    tools=[generate_sales_chart],
)

a2a_app = to_a2a(root_agent, port=8002)
