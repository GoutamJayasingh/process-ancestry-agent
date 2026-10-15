from mcp.server.fastmcp import FastMCP

from tools.process_lookup import find_process
from tools.process_tree import get_process_tree

mcp = FastMCP("process-ancestry-agent")


@mcp.tool()
def search_processes(name: str) -> list[dict]:
    """Find Linux processes matching a process name."""
    if not name or not name.strip():
        raise ValueError("Process name cannot be empty.")
    return find_process(name.strip())


@mcp.tool()
def trace_process_ancestry(name: str) -> list[dict]:
    """Find processes by name and return their parent ancestry chains."""
    if not name or not name.strip():
        raise ValueError("Process name cannot be empty.")
    return get_process_tree(name.strip())


if __name__ == "__main__":
    mcp.run(transport="stdio")
