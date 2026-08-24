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
    return search_sources


