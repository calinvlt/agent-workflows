import asyncio

from agents import Agent, Runner
from agents.mcp import MCPServerStdio

from openai_client import init_client

init_client()

thinking_srv = MCPServerStdio(
    name="seq-think",
    params={
        "command": "npx",
        "args": [
            "-y",
            "@modelcontextprotocol/server-sequential-thinking"
        ]
    }
)

prompt="""
You are a helpful assistant
"""

agent=Agent(name="Assistant", instructions=prompt, mcp_servers=[thinking_srv])

async def main():
    async with thinking_srv:
        tools = await thinking_srv.list_tools()
        print("Available tools", tools)

        goal = "Discover and output the tools and functions you have available."
        print("Running..", goal)
        result = await Runner.run(agent, goal)
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())

