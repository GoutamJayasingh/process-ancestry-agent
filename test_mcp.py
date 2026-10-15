import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            response = await session.list_tools()
            print("Available MCP tools:")
            for tool in response.tools:
                print(f"- {tool.name}: {tool.description}")

            print("\nTesting search_processes...")
            result = await session.call_tool(
                "search_processes",
                {"name": "bash"},
            )
            print(result)


if __name__ == "__main__":
    asyncio.run(main())
