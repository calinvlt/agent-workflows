from typing_extensions import TypedDict

from pydantic import BaseModel, ConfigDict

class Task(TypedDict):    #1
    id: int
    description: str

class ResearchPlanModel(BaseModel):
    tasks: list[Task]
    model_config = ConfigDict(extra='forbid')