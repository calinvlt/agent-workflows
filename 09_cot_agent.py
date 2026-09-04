from agents import Agent

from openai_client import init_client, run_agent

init_client()

cot_agent = Agent(
    name="TimeTravelerCoT",
    instructions=(
        "You are a time traveler problem solver."
        "Work out the soltion step by step, then give the final answer."
    )
)

question = (
    "Starting in 2025, you travel 10 years to the past, then 5 years to the future. "
    "What year do you end up in?"
)

run_agent(cot_agent, question)