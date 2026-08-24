import os
import asyncio
import sys

from agents import Agent, Runner

from openai_client import client

instructions = """
You are a research planning assistant.

***TASK INSTRUCTIONS*
- You will be given a research topic
- Your task is to provide a plan on how to resrarch this topic.
- Output 5 concise tasks (10 words or less) to your plan.
"""

agent = Agent(
    name="Research Planner",
    instructions=instructions,
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
)

input = "learn about digging for the truth"

async def main():
    result = await Runner.run(
        agent,
        input=input,
    )

    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
