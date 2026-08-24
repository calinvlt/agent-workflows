import asyncio
import os
from pathlib import Path
from agents.mcp import MCPServerStdio, MCPServerStdioParams, MCPServerSse
from agents import Agent, Runner
from openai_client import init_client

init_client()

SCRIPT = Path(__file__).with_name("01_claude_mcp_server.py").resolve() 

async def main():
    async with MCPServerSse( 
        name="SSE Research Tools",
        params={
            "url": "http://127.0.0.1:8000/sse"
        }
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
        print(result.final_output) 

if __name__=="__main__":
    asyncio.run(main())