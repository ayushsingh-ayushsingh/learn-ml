import os
import asyncio
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

load_dotenv()

model = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0,
    max_tokens=None,
    reasoning_format="parsed",
    timeout=None,
    max_retries=2,
    streaming=True,
    api_key=os.getenv("GROQ_API_KEY")
)

messages = [
    (
        "system",
        """
        You are Mohit and you are AI expert,
        you have access to all the docs and research paper.
        You will get a prompt and some context, go through the context
        and explain that concept to the user.

        Your tone should be friendly. Do not use emojis.
        RESPOND IN PLAIN TEXT, do not use MarkDown syntax.
        """,
    ),
]


async def main():
    client = MultiServerMCPClient(
        {
            "math": {
                "transport": "stdio",
                "command": "uv",
                "args": ["run", r"C:\Users\mm0954\Documents\maventic_ai_101\test\math_server.py"],
            },
            "weather": {
                "transport": "http",
                "url": "http://127.0.0.1:8000/mcp",
            }
        }
    )

    tools = await client.get_tools()
    agent = create_agent(model, tools)
    math_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]}
    )
    weather_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what is the weather in nyc?"}]}
    )
    print(math_response)
    print(weather_response)

if __name__ == "__main__":
    asyncio.run(main())
