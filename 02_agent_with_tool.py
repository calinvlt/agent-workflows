import os
from typing import TypedDict
from agents import Agent, function_tool
from openai import BaseModel
from pydantic import ConfigDict

from openai_client import init_client, run_agent
from output_types_basic import ResearchPlanModel

prompt = """
You are a research planning assistant.

**TASK INSTRUCTIONS**
- You will be given a research topic
- Begin by using the tool get_research_sources() to get a list of available research sources.
- Constrain your research plan to only use the available research resources.
- Your task is to provide a plan to researching this topic.
- Output 5 concise tasks and specify which of the available research sources will be used for each task.
"""

class Task(TypedDict):
    step: int
    """Task Step."""
    research_source: str
    """The source to search"""
    description: str
    """Task description"""

class ResearchPlanModel(BaseModel):
    tasks: list[Task]
    """Numbered tasks for research"""
    model_config = ConfigDict(extra='forbid')

@function_tool
def get_research_source() -> list[str]:
    """Provides a list o research source"""
    search_sources = ["Wikipedia", "Google", "YouTube"]
    return search_sources


init_client()

agent = Agent(
    name="Research Planner",
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    instructions=prompt,
    output_type=ResearchPlanModel,
    tools=[get_research_source]
)
run_agent(agent, "learn about OOP")