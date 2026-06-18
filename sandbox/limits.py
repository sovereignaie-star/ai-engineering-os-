from dataclasses import dataclass

@dataclass
class SandboxLimits:
    max_execution_time: int = 300  # seconds
    max_memory_mb: int = 1024
    max_files: int = 100
    max_file_size_mb: int = 10
    allowed_directories: list = None
    blocked_commands: list = None

    def __post_init__(self):
        if self.allowed_directories is None:
            self.allowed_directories = ["/workspace", "/tmp"]
        if self.blocked_commands is None:
            self.blocked_commands = ["rm -rf", "sudo", "chmod 777", "dd", "mkfs"]

class SandboxValidator:
    def __init__(self, limits: SandboxLimits = None):
        self.limits = limits or SandboxLimits()

    def validate_command(self, command: str) -> bool:
        for blocked in self.limits.blocked_commands:
            if blocked in command:
                return False
        return True

    def validate_path(self, path: str) -> bool:
        for allowed in self.limits.allowed_directories:
            if path.startswith(allowed):
                return True
        return False
