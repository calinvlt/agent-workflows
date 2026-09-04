from agents import Agent

from openai_client import init_client, run_agent

init_client()

generator = Agent(
    name="ToT-generator",
    instructions="Guven the current situation, brainstorm a possible next step or action the reach the goal."
)

evaluator = Agent(
    name="ToT-evaluator",
    instructions="Assess how likely the proposed plan will solve the problem. Respond with 'promising' or 'unlikely'."
)

problem="""
You need to reach the year 1800 from 2025 using a time machine that can jump either -100 or -30 years.
"""

initial_thoughts = []
for i in range(10):
    resp = run_agent(generator, input=f"Problem: {problem}\nThink of a first step.")
    initial_thoughts.append(resp)

promising_branches = []
for thought in initial_thoughts:
    eval_resp = run_agent(evaluator, input=f"Plan: {thought}\nIs this promising?")
    if 'promising' in eval_resp:
        next_step = run_agent(generator, input=f"Current idea: {thought}\nNext steps?")
        promising_branches.append(f"{thought} -> {next_step}")

print("initial thought candidates:", initial_thoughts)
print('Expanded promising branch:', promising_branches[0] if promising_branches else "None")