from pathlib import Path

from tools.process_info import get_process_info


PROC_ROOT = Path("/proc")


def find_process(name: str) -> list[dict]:
    """Find Linux processes whose names match the supplied name."""

    name = name.strip()

    if not name:
        raise ValueError("Process name cannot be empty.")

    matches = []

    for entry in PROC_ROOT.iterdir():
        if not entry.name.isdigit():
            continue

        pid = int(entry.name)

        try:
            info = get_process_info(pid)
        except (ProcessLookupError, PermissionError, ValueError):
            # The process may have exited or become unavailable.
            continue

        if info["name"].casefold() == name.casefold():
            matches.append(info)

    return sorted(matches, key=lambda process: process["pid"])
