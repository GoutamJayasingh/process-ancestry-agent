from pathlib import Path

PROC_ROOT = Path("/proc")


def get_process_info(pid: int) -> dict:
    """Return the PID, name, and parent PID of a Linux process."""

    if pid <= 0:
        raise ValueError("PID must be a positive integer.")

    stat_path = PROC_ROOT / str(pid) / "stat"

    try:
        stat_content = stat_path.read_text()
    except FileNotFoundError as exc:
        raise ProcessLookupError(
            f"Process with PID {pid} does not exist."
        ) from exc

    # A process name may contain spaces or parentheses.
    # Find the final ')' before parsing the remaining fields.
    closing_paren = stat_content.rfind(")")
    opening_paren = stat_content.find("(")

    if opening_paren == -1 or closing_paren == -1:
        raise ValueError(f"Could not parse stat data for PID {pid}.")

    process_name = stat_content[opening_paren + 1:closing_paren]
    remaining_fields = stat_content[closing_paren + 1:].split()

    # After the process name:
    # index 0 = process state (field 3)
    # index 1 = PPID (field 4)
    if len(remaining_fields) < 2:
        raise ValueError(f"Incomplete stat data for PID {pid}.")

    try:
        parent_pid = int(remaining_fields[1])
    except ValueError as exc:
        raise ValueError(f"Invalid PPID for PID {pid}.") from exc

    return {
        "pid": pid,
        "name": process_name,
        "ppid": parent_pid,
    }
