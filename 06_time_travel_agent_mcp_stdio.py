import asyncio
import os
from pathlib import Path
from agents.mcp import MCPServerStdio, MCPServerStdioParams
from agents import Agent, Runner
from openai_client import init_client

init_client()

prompt = """
You are a time tracking journaling agent. 
Always use the 'load_journal' tool at the start to get past entries.
For a new event, call 'record_event' tool to save it.
If asked for a summary or to show the journal, output all records events.
"""

travel_events = [
    "Traveled to ancient Greece and talk with a great philosopher.",
    "Visited the Library of Alexandria.",
    "Went to the moon in 1969"
]

SCRIPT = Path(__file__).with_name("06_mcp_time_travel_tracker.py").resolve()

async def main():
    async with MCPServerStdio(
        name="Time Tracker Server",
        params=MCPServerStdioParams(command="mcp", args=["run", str(SCRIPT)])
    ) as time_tracker_server:
        agent=Agent(
            name="Assistant",
            model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
            instructions=prompt,
            mcp_servers=[time_tracker_server]
        )
        for event in travel_events:
                await Runner.run(agent, event)
        result = await Runner.run(agent, "Show me travel history")
        print(result.final_output)
    
if __name__=="__main__":
    asyncio.run(main())