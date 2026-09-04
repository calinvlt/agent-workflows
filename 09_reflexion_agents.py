from agents import Agent, RunContextWrapper

from openai_client import init_client, run_agent

init_client()

problem = (
    "I left the year 2000 in a time machine, went forward 30 years, "
    "then back 40 years. I claim I'm now in 1990. Am I correct?"
)
problem = """
In a sci-fi film, Alex is a time traveler who decides to go back in time
to witness a famous historical event that took place 100 years ago,
which lasted for 10 days. He arrives three days before the event starts.
However, after spending six days in the past, he jumps forward in time
by 50 years and stays there for 20 days. Then, he travels back to
witness the end of the end. 
How many days does Alex spend in the past before he sees the end of the event?
"""
TARGET_DAYS = "26"  # expected final answer
MAX_ATTEMPTS = 6  # fail-safe cap on retries

def get_reflextion_solver_instructions(
    run_context: RunContextWrapper, agent: Agent
) -> str:
    """Generate instructions for the reflexion solver agent"""
    instructions = (
        "You are a time-traveler expert. Solve the problem step by step "
        "and be careful to avoid mistakes."
    )
    return instructions + "\nHINT:\n" + run_context.context

solver=Agent(name="TimeTravelerReflexion", instructions=get_reflextion_solver_instructions)
critic=Agent(name="TimeTravelerCritic", instructions=(
    "You are an expert tutor. If the solution is wrong, explain the error "
    "and give a concise hint for improvement."
))

# solver loop
feedback_hint=''

for attempt_no in range(1, MAX_ATTEMPTS):
    answer = run_agent(solver, input=problem, context=feedback_hint)

    is_correct = TARGET_DAYS in answer
    says_claim_correct = "yes" in answer.lower() or "correct" in answer.lower()
    solved = is_correct and says_claim_correct

    if solved:
        print("Solution accepted.")
        break

    feedback_prompt = (
        f"Solution given:\n{answer}\n\n"
        f"Expected final daus: {TARGET_DAYS}\n"
        "Explain the error briefly and give a helpful hint."
    )

    hint = run_agent(critic, input=feedback_prompt)
    print(f"Feedback hint:{hint}")
    feedback_hint=hint
else:
    print("\n Max attempts reached")