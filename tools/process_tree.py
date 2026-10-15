from tools.process_lookup import find_process
from tools.ancestry import get_process_ancestry


def get_process_tree(name: str) -> list[dict]:
    """Find processes by name and return their ancestry chains."""

    matches = find_process(name)
    results = []

    for process in matches:
        pid = process["pid"]

        try:
            ancestry = get_process_ancestry(pid)
        except (ProcessLookupError, PermissionError, ValueError) as exc:
            results.append({
                "process": process,
                "ancestry": [],
                "error": str(exc),
            })
            continue

        results.append({
            "process": process,
            "ancestry": ancestry,
        })

    return results
