import pytest
from tools.guardrails import is_dangerous_command


@pytest.mark.parametrize(
    "command",
    [
        "rm -rf /",
        "rm -fr /tmp/example",
        "rm -r -f /tmp/example",
        "sudo apt update",
        "mkfs.ext4 /dev/sda1",
        "dd if=/dev/zero of=/dev/sda",
        "echo test > /dev/sda",
        "shutdown now",
        "reboot",
        "SUDO apt update",
        "MKFS.EXT4 /dev/sda1",
    ],
)
def test_detects_dangerous_patterns(command):
    assert is_dangerous_command(command)


@pytest.mark.parametrize(
    "command",
    [
        "ls -l",
        "python --version",
        "show system statistics",
        "find process named bash",
        "rm -r /tmp/example",
        "rm -f /tmp/example",
    ],
)
def test_allows_unmatched_inputs(command):
    assert not is_dangerous_command(command)


@pytest.mark.parametrize("command", ["", "   ", None, 123])
def test_rejects_invalid_inputs(command):
    assert is_dangerous_command(command)
