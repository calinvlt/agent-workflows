import asyncio
import os
from agents.mcp import MCPServerStdio
from agents import Agent, Runner, function_tool
from openai_client import init_client

init_client()

_journal=[]

@function_tool
def record_entry(entry: str) -> dict:
    """Add a new travel event to the journal"""
    _journal.append(entry)
    print(f"Event recorded: {entry}")
    return {"status": "recorded", "entry": entry}

@function_tool
def load_journal() -> dict:
    """Load the current travel journal entries"""
    print("Loading the journal entries")
    return {"status": "loaded", "journal": "\n".join(_journal)}

prompt = """
You are a time tracking journaling agent. 
Always use the 'load_journal' tool at the start to get past entries.
For a new event, call 'record_event' tool to save it.
If asked for a summary or to show the journal, output all records events.
"""

agent = Agent(
    name="Time Tracker Agent",
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    instructions=prompt,
    tools=[record_entry, load_journal]
)

travel_events = [
    "Traveled to ancient Greece and talk with a great philosopher.",
    "Visited the Library of Alexandria.",
    "Went to the moon in 1969"
]

async def main():
    print("Recording travels")
    for event in travel_events:
        await Runner.run(agent, event)
    result = await Runner.run(agent, "Show me travel history")
    print(result.final_output)

asyncio.run(main())