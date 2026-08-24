# Agents

## Setup
Install Docker and VS Code then open the folder in VS Code and install the recommended extensions.

In Microsoft Foundry create a new deployment and add `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_KEY` and `AZURE_OPENAI_DEPLOYMENT` to your machine environment variables.

Start the dev container.

## First agent
Contains a simple agent using a Azure OpenAI model

## 05_time_travel_agency.py
Demonstrates the concept of temporary memory or scratchpad for agents.
`_journal` is kept in memory for later retrieval by the summarization tool.

## 06 Time Travel Agent
This is about moving the tools into a MCP server.

- `06_mcp_time_travel_tracker.py` contains the code for the MCP server using FastMCP library.
- `06_time_travel_agent_mcp_stdio.py` hosts the MCP server in process using `stdio` to communicate.
- `06_time_travel_agent_mcp_sse.py` hosts the MCP server in a separate process started with `mcp run -t sse 06_mcp_time_travel_tracker.py` and it's using `sse` or Server-Side-Events to communicate.

