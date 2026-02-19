import json
import asyncio

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

client = MultiServerMCPClient(
    {
        "file_creator": {
            "transport": "http",
            "url": "http://localhost:8003/mcp",
        }
    }
)


async def main():
    tools = await client.get_tools()

    # tools_json = json.dumps(
    #     [tool.model_dump() for tool in tools],
    #     indent=2,
    #     default=str
    # )
    # print("Tools JSON:")
    # print(tools_json)

    # print("\nAttempting to create file...")

    try:
        result = await tools[0].ainvoke(
            {"file_name": "manual_test.md",
                "content": "# Success\nThis file was created without an LLM agent!"}
        )

        for block in result:
            if hasattr(block, 'text'):
                print(f"Server Response: {block.text}")
            else:
                print(f"Server Response: {block}")

    except Exception as e:
        print(f"Error executing tool: {e}")

if __name__ == "__main__":
    asyncio.run(main())
