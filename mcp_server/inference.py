import json
import asyncio

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_groq import ChatGroq

load_dotenv()

client = MultiServerMCPClient(
    {
        "weather": {
            "transport": "http",
            "url": "http://localhost:8000/mcp",
        }
    }
)

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    max_retries=2,
    timeout=None,
    max_tokens=None,
    streaming=True
)


async def main():
    tools = await client.get_tools()
    prompts = await client.get_prompt()
    resources = await client.get_resources()
    
    tools_json = json.dumps(
        [tool.model_dump() for tool in tools],
        indent=2,
        default=str
    )
    print("Tools JSON:")
    print(tools_json)
    
    # agent = create_agent(
    #     llm,
    #     tools,
    #     system_prompt="You are a helpful assistant."
    # )
    # messages = [
    #     HumanMessage(content="what is the weather in nyc?"),
    # ]
    # response = await agent.ainvoke({"messages": messages})
    # final_message = response["messages"][-1]
    # final_answer = final_message.content
    # print("Response:", final_answer)

if __name__ == "__main__":
    asyncio.run(main())
