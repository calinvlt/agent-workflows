import asyncio
import os
from pathlib import Path
from agents.mcp import MCPServerStdio, MCPServerStdioParams
from agents import Agent, Runner
from openai_client import init_client

init_client()

SCRIPT = Path(__file__).with_name("01_claude_mcp_server.py").resolve() #1

async def main():
    async with MCPServerStdio( #2
        name="Research Tools",
        params=MCPServerStdioParams(
            command="mcp",
            args=["run", str(SCRIPT)] #2
        )
    ) as research_server:
        agent = Agent(
            name="Assistant",
            model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
            instructions="Use the research tools to perform search",
            mcp_servers=[research_server]
        )

        print('Running: Get available research sources')
        result = await Runner.run(
            agent,
            "Get available research sources"
        )
        print(result.final_output) #3

if __name__=="__main__":
    asyncio.run(main())