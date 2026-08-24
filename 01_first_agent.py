import os
from agents import Agent, ModelSettings

from openai_client import init_client, run_agent
from output_types_basic import ResearchPlanModel

init_client()

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
    model_settings=ModelSettings(
        temperature=0.0,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.5
    ),
    output_type=ResearchPlanModel,
)

run_agent(agent, "learn about woodworking safety")