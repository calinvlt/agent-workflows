import asyncio
from pathlib import Path
from agents.mcp import MCPServerStdio, MCPServerStdioParams
from agents import Agent, Runner
from openai_client import init_client

SCRIPT = Path(__file__).with_name("01_claude_mcp_server.py").resolve()

servers = [
    MCPServerStdio(
        name="Research Tool", 
        params=MCPServerStdioParams(command='mcp', args=["run", str(SCRIPT)])
    ),
    MCPServerStdio(
        name="sequential-thinking", 
        params=MCPServerStdioParams(command='npx', args=["-y", "@modelcontextprotocol/server-sequential-thinking"])
    ),
    MCPServerStdio(
        name="filesystem", 
        params=MCPServerStdioParams(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem", str(Path(__file__).parent.resolve())]
        )
    ),
]

prompt = """
You are a research assistant who can use tools to perform and plan research.
Given a research goal, use the research tools to find research resources.
Then, use the sequential thinking tool to plan the research.
Finally, use the filesystem tool to write the research plan as a text file.
"""

async def main():
    init_client()

    async with (
        servers[0] as research_srv,
        servers[1] as thinking_srv,
        servers[2] as fs_srv
    ):
        agent = Agent(
            name="Assistant",
            instructions=prompt,
            mcp_servers=[research_srv, thinking_srv, fs_srv]
        )
        goal = """Produce a research plan to find the book: 'The Hitchhiker's Guide to the Galaxy'"""
        print("Running ...", goal)
        result = await Runner.run(agent, goal)
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())