import os

from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, set_default_openai_client

load_dotenv()

def init_client():
    client = AsyncOpenAI(
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
    )

    set_default_openai_client(client)


def run_agent(agent: Agent, input: str, context=None):    
    result = Runner.run_sync(
        agent,
        input=input,
        context=context
    )
    print(result.final_output)
    return result.final_output

async def run_agent_async(agent: Agent, input: str):
    result = await Runner.run(
        agent,
        input=input,
    )
    print(result.final_output)