import asyncio
from pathlib import Path
from agents.mcp import MCPServerStdio, MCPServerStdioParams
from agents import Agent, Runner
from agents.extensions.visualization import draw_graph
from openai_client import init_client

SCRIPT = Path(__file__).with_name("08_variable_research_tools.py").resolve()

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
    instructions="""You are a research assistant. 
Your role is to find research sources. 
Do not make up or invent any research sources.
Always hand off to the thinking agent.
"""
)

thinking_agent = Agent(
    name="Thinking Agent",
    instructions="""You are a research planning assistant. 
Your role is to plan the research.
You will receive a list of research sources from the research agent.
Use the sequentialThinking tool to create a research plan based on the sources.
Always hand off to the filesystem agent.
""",    
)

fs_agent = Agent(
    name="Filesystem Agent",
    instructions="""You are a filesystem assistant. 
Your role is to write the research plan as a text file. 
Never make up or invent any ouput.""",    
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
        research_agent.handoffs=[thinking_agent]        
                
        thinking_agent.mcp_servers=[thinking_srv]
        thinking_agent.handoffs=[fs_agent]
        
        fs_agent.mcp_servers=[fs_srv]

        draw_graph(research_agent).view() 
        input("Press Enter to continue")

        result = await Runner.run(research_agent, goal, max_turns=25)
        print(result.final_output)

asyncio.run(research())