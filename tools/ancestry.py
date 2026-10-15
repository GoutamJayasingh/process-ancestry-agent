
from tools.process_info import get_process_info


def get_process_ancestry(pid: int, max_depth: int = 100) -> list[dict]:
    """Return a process and its ancestors, starting from the given PID."""

    if pid <= 0:
        raise ValueError("PID must be a positive integer.")

    if max_depth <= 0:
        raise ValueError("max_depth must be a positive integer.")

    ancestry = []
    visited = set()
    current_pid = pid

    for _ in range(max_depth):
        if current_pid in visited:
            break

        visited.add(current_pid)

        info = get_process_info(current_pid)
        ancestry.append(info)

        # Stop when we reach the root process.
        if current_pid == 1:
            break

        parent_pid = info["ppid"]

        if parent_pid <= 0:
            break

        current_pid = parent_pid

    return ancestry
