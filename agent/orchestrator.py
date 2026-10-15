import asyncio
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from agent.llm_client import client, MODEL
from tools.guardrails import confirm_tool_call


SYSTEM_PROMPT = """
You are a Linux process ancestry assistant.
You can use these tools:
- search_processes: find Linux processes by name.
- trace_process_ancestry: find matching processes and their parent ancestry.

Use a tool when the user asks about actual running processes.
Never invent PIDs or process information.
Explain the results clearly.
"""


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_processes",
            "description": "Find running Linux processes matching a name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Process name to search for",
                    }
                },
                "required": ["name"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "trace_process_ancestry",
            "description": "Find processes by name and trace their parent ancestry.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Process name to trace",
                    }
                },
                "required": ["name"],
                "additionalProperties": False,
            },
        },
    },
]


async def ask_agent(question: str) -> str:
    if not question.strip():
        return "Please enter a question."

    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question},
            ]

            for _ in range(5):
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    tools=TOOLS,
                    tool_choice="auto",
                )

                message = response.choices[0].message
                messages.append(message.model_dump(exclude_none=True))

                if not message.tool_calls:
                    return message.content or "No response was returned."

                for tool_call in message.tool_calls:
                    tool_name = tool_call.function.name

                    if tool_name not in {
                        "search_processes",
                        "trace_process_ancestry",
                    }:
                        tool_result = {"error": "Unknown tool"}
                    else:
                        try:
                            arguments = json.loads(
                                tool_call.function.arguments
                            )
                            if not isinstance(arguments, dict):
                                raise ValueError("Tool arguments must be a JSON object.")
                            if set(arguments) != {"name"}:
                                raise ValueError("Only the 'name' argument is allowed.")

                            name = arguments["name"]
                            if not isinstance(name, str) or not name.strip():
                                raise ValueError("A non-empty process name is required.")

                            approved = confirm_tool_call(
                                tool_name, {"name": name.strip()}
                            )
                            if not approved:
                                tool_result = {
                                    "status": "rejected",
                                    "message": "Tool call cancelled by user."
                                }
                            else:
                                result = await session.call_tool(
                                    tool_name,
                                    {"name": name.strip()},
                                )
                                if result.isError:
                                    tool_result = {
                                        "error": "The MCP tool returned an error."
                                    }
                                else:
                                    tool_result = [
                                        item.text
                                        for item in result.content
                                        if hasattr(item, "text")
                                    ]
                        except (ValueError, TypeError, json.JSONDecodeError) as exc:
                            tool_result = {"error": str(exc)}
                        except Exception:
                            tool_result = {
                                "error": "The process tool call failed."
                            }

                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps(tool_result),
                        }
                    )

            return "I reached the tool-call limit. Please try a simpler question."


def run_question(question: str) -> str:
    return asyncio.run(ask_agent(question))
