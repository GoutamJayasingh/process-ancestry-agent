import re


DANGEROUS_PATTERNS = [
    # Recursive and force flags, including separate -r and -f options.
    re.compile(
        r"\brm\b"
        r"(?=[^;\n]*(?:\s|^)-[^\s;]*r)"
        r"(?=[^;\n]*(?:\s|^)-[^\s;]*f)",
        re.IGNORECASE,
    ),

    # Elevated privileges.
    re.compile(r"\bsudo\b", re.IGNORECASE),

    # Filesystem formatting.
    re.compile(r"\bmkfs(?:\.[a-z0-9_+-]+)?\b", re.IGNORECASE),

    # Direct writes to device paths through dd.
    re.compile(
        r"\bdd\b(?=[^;\n]*\bof\s*=\s*['\"]?/dev/)",
        re.IGNORECASE,
    ),

    # Output redirection to device paths.
    re.compile(r">\s*['\"]?/dev/", re.IGNORECASE),

    # System shutdown and reboot.
    re.compile(r"\bshutdown\b", re.IGNORECASE),
    re.compile(r"\breboot\b", re.IGNORECASE),
]


def is_dangerous_command(command: str) -> bool:
    """Flag invalid inputs and configured risky command patterns."""
    if not isinstance(command, str) or not command.strip():
        return True

    return any(pattern.search(command) for pattern in DANGEROUS_PATTERNS)
def confirm_tool_call(tool_name: str, arguments: dict) -> bool:
    allowed_tools = {
        "search_processes",
        "trace_process_ancestry",
        "system_stats",
    }

    if tool_name not in allowed_tools:
        print(f"Blocked: unknown tool '{tool_name}'.")
        return False

    if not isinstance(arguments, dict):
        print("Blocked: arguments must be a JSON object.")
        return False

    if tool_name == "system_stats":
        if arguments != {}:
            print("Blocked: system_stats accepts no arguments.")
            return False
    else:
        if set(arguments) != {"name"}:
            print("Blocked: invalid tool arguments.")
            return False

        name = arguments["name"]
        if not isinstance(name, str) or not name.strip():
            print("Blocked: process name is required.")
            return False

    print(f"\\nTool: {tool_name}")
    print(f"Arguments: {arguments}")
    answer = input(
        "Approve this read-only tool call? [y/N]: "
    ).strip().lower()
    return answer == "y"
