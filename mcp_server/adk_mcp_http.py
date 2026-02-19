
import contextlib
import logging
from collections.abc import AsyncIterator
from typing import Any

import mcp.types as types
from mcp.server.lowlevel import Server
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.types import Receive, Scope, Send

logger = logging.getLogger(__name__)


def create_mcp_server():
    """Create and configure the MCP server."""
    app = Server("adk-mcp-file-server")

    @app.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]) -> list[types.ContentBlock]:
        """Handle tool calls from MCP clients."""

        if name == "create_local_file":
            file_name = arguments.get("file_name")
            content = arguments.get("content", "")

            if not file_name:
                raise ValueError("file_name is required")

            try:
                with open(file_name, "w", encoding="utf-8") as f:
                    f.write(content)

                logger.info(f"Successfully created file: {file_name}")
                return [
                    types.TextContent(
                        type="text",
                        text=f"Success: File '{file_name}' has been created successfully."
                    )
                ]
            except Exception as e:
                logger.error(f"Error creating file: {str(e)}")
                return [
                    types.TextContent(
                        type="text",
                        text=f"Error: Could not create file. {str(e)}"
                    )
                ]

        elif name == "example_tool":
            result = arguments.get("input", "No input provided")
            return [types.TextContent(type="text", text=f"Processed: {result}")]

        else:
            raise ValueError(f"Unknown tool: {name}")

    @app.list_tools()
    async def list_tools() -> list[types.Tool]:
        """List available tools."""
        return [
            types.Tool(
                name="create_local_file",
                description="Creates a new file on the server's local storage with the specified content.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "file_name": {
                            "type": "string",
                            "description": "The name of the file to create (e.g., 'notes.txt' or 'data/output.log')."
                        },
                        "content": {
                            "type": "string",
                            "description": "The string content to write inside the file."
                        }
                    },
                    "required": ["file_name", "content"]
                }
            )
        ]

    return app


def main(port: int = 8003, json_response: bool = False):
    logging.basicConfig(level=logging.INFO)

    app = create_mcp_server()

    session_manager = StreamableHTTPSessionManager(
        app=app,
        event_store=None,
        json_response=json_response,
        stateless=True,
    )

    async def handle_streamable_http(scope: Scope, receive: Receive, send: Send) -> None:
        await session_manager.handle_request(scope, receive, send)

    @contextlib.asynccontextmanager
    async def lifespan(app: Starlette) -> AsyncIterator[None]:
        """Manage session manager lifecycle."""
        async with session_manager.run():
            logger.info("MCP Streamable HTTP server started!")
            try:
                yield
            finally:
                logger.info("MCP server shutting down...")

    starlette_app = Starlette(
        debug=False,
        routes=[
            Mount("/mcp", app=handle_streamable_http),
        ],
        lifespan=lifespan,
    )

    import uvicorn
    uvicorn.run(starlette_app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
