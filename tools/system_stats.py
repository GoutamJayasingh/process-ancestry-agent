"""Read-only Linux system statistics."""
import os
import time


def get_system_stats() -> dict:
    """Return CPU load, memory information, and uptime."""
    with open("/proc/loadavg", encoding="utf-8") as f:
        load = f.read().split()

    memory = {}
    with open("/proc/meminfo", encoding="utf-8") as f:
        for line in f:
            key, value = line.split(":", 1)
            if key in {"MemTotal", "MemAvailable"}:
                memory[key] = int(value.strip().split()[0])

    with open("/proc/uptime", encoding="utf-8") as f:
        uptime_seconds = float(f.read().split()[0])

    return {
        "cpu_load_average_1_5_15_min": [float(x) for x in load[:3]],
        "memory_total_mb": round(memory["MemTotal"] / 1024, 2),
        "memory_available_mb": round(memory["MemAvailable"] / 1024, 2),
        "uptime_seconds": int(uptime_seconds),
    }
