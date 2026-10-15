from tools.guardrails import is_dangerous_command, confirm_tool_call

def test_dangerous_commands_are_detected():
    assert is_dangerous_command("rm -rf /")
    assert is_dangerous_command("sudo reboot")
    assert is_dangerous_command("mkfs.ext4 /dev/sda")

def test_safe_command_is_not_flagged():
    assert not is_dangerous_command("ps aux")

def test_empty_command_is_rejected():
    assert is_dangerous_command("")

def test_unknown_tool_is_rejected(monkeypatch):
    assert not confirm_tool_call("delete_everything", {"name": "bash"})

def test_invalid_arguments_are_rejected(monkeypatch):
    assert not confirm_tool_call("search_processes", {"unexpected": "value"})
