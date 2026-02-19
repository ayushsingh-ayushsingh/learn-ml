# Learning AI/ML Development

## Example - 1

A toy project implementing A2A Protocol with Google Agent Development kit on local network

![ADK A2A](./learn_adk/adk-a2a-demo.png)

## Example - 2

A toy project implementing MCP (stdio), A2A Protocol with ADK

![MCP ADK A2A](./learn_adk/adk-a2a-mcp.png)

## Example - 3

Implementing MCP over HTTP transport in previus project

![MCP ADK A2A](./learn_adk/adk-a2a-mcp-http-2.png)

# Scripts

Scripts to run different sections of the project
For all the commands below I recommend using different terminals, and start from the root directory.

## Bun server for database endpoints

Bun server runs on http://0.0.0.0:3000

```bash
cd server
bun dev
```

## Database Agent - CRUD over HTTP

DB Agent is exposed on http://0.0.0.0:8001 via A2A

```bash
cd learn_adk
uvicorn db_agent.agent:a2a_app --host 0.0.0.0 --port 8001
```

## Chart Agent - Creates line chart for 2D Data

Chart Agent is exposed on http://0.0.0.0:8002 via A2A

```bash
cd learn_adk
uvicorn chart_agent.agent:a2a_app --host 0.0.0.0 --port 8002
```

## File Creation Tool - MCP HTTP Server

File creation MCP server is exposed on http://0.0.0.0:8003 via HTTP transport

```bash
cd mcp_server
uv run adk_mcp_http.py
```

## Web Scraper tool STDIO*

Web Scraping MCP server based on standard input output transport
!Not required to run on any port since it runs over STDIO 

## Orchestrator Agent

Agent to orchestrate all the other agents

```bash
cd learn_adk
adk run orchestrator
```

Test agents on web using adk cli, defaults at port 8000

```bash
cd learn_adk
adk web
```

---

Crafted with ♥️ by Ayush Singh
