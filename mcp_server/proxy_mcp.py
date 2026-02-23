from fastmcp import FastMCP

mcp = FastMCP.as_proxy(
    "http://127.0.0.1:8003/mcp",
    name="file_system_mcp_server"
)

if __name__ == "__main__":
    mcp.run()
