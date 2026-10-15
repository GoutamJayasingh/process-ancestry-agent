import re

DANGEROUS_PATTERNS = [
    r"\brm\s+-[a-zA-Z]*r[a-zA-Z]*f\b",
    r"\bsudo\b",
    r"\bmkfs(?:\.\w+)?\b",
    r"\bdd\s+if=",
    r">\s*/dev/",
    r"\bshutdown\b",
    r"\breboot\b",
]

def is_dangerous_command(command: str) -> bool:
    if not isinstance(command, str) or not command.strip():
        return True
    return any(
        re.search(pattern, command, re.IGNORECASE)
        for pattern in DANGEROUS_PATTERNS
    )

def confirm_tool_call(tool_name: str, arguments: dict) -> bool:
    if tool_name not in {"search_processes", "trace_process_ancestry"}:
        print(f"Blocked: unknown tool '{tool_name}'.")
        return False
    if not isinstance(arguments, dict) or set(arguments) != {"name"}:
        print("Blocked: invalid tool arguments.")
        return False
    name = arguments["name"]
    if not isinstance(name, str) or not name.strip():
        print("Blocked: process name is required.")
        return False

    print(f"\nTool: {tool_name}")
    print(f"Arguments: {arguments}")
    answer = input("Approve this read-only tool call? [y/N]: ").strip().lower()
    return answer == "y"
