import asyncio
import os
from agents.mcp import MCPServerStdio
from agents import Agent, Runner
from openai_client import init_client

async def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    init_client()

    async with MCPServerStdio(
        name="FS via npx",
        params={
            "command":"npx", 
            "args": ["-y", "@modelcontextprotocol/server-filesystem", current_dir]
        }
    ) as fs_server:
        agent = Agent(
            name="FS Agent",
            model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
            instructions="Use the filesystem tool to help the user with their tasks",
            mcp_servers=[fs_server]
        )
        print("Running the agent to get the files")
        result = await Runner.run(
            agent,
            "List the files in the current folder"
        )
        print(result.final_output)

if __name__=="__main__":
    asyncio.run(main())