import random

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Research Tools")

@mcp.tool()
def get_research_sources() -> list[str]:
    "Providesd a list of research sources"
    search_sources = [
        "Wikipedia",
        "Google",
        "YouTube"
    ]

    num_sources = random.randint(0, 3)
    if (num_sources == 0):
        return []
    return random.sample(search_sources, num_sources)