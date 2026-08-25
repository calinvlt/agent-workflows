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

research_agent = Agent(
    name="Research Agent",
    instructions="You are a research assistant. Your role is to find research sources",    
)

thinking_agent = Agent(
    name="Thinking Agent",
    instructions="You are a research assistant. Your role is to plan the research.",    
)

fs_agent = Agent(
    name="Filesystem Agent",
    instructions="You are a research assistant. Your role is to write the research plan as a text file.",    
)

async def research():
    init_client()

    async with(
        servers[0] as research_srv,
        servers[1] as thinking_srv,
        servers[2] as fs_srv
    ):
        goal = """Produce a research plan to find the book 'The Hitchhiker's Guide to the Galaxy'"""
        print("Running ...", goal)

        research_agent.mcp_servers=[research_srv]
        result = await Runner.run(research_agent, goal)        

        thinking_agent.mcp_servers=[thinking_srv]
        result = await Runner.run(thinking_agent, result.final_output)
        
        fs_agent.mcp_servers=[fs_srv]
        result = await Runner.run(fs_agent, result.final_output)        

        print(result.final_output)

asyncio.run(research())