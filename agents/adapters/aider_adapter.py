"""
Aider Adapter
"""

import subprocess
import os

class AiderAdapter:
    def __init__(self, config):
        self.config = config

    def execute_task(self, task: dict) -> dict:
        command = [
            "aider",
            "--message", task["description"],
            "--model", self.config.get("model", "gpt-4"),
            "--yes"
        ]
        result = subprocess.run(command, capture_output=True, text=True, cwd=task.get("workspace", "."))
        return {
            "status": "success" if result.returncode == 0 else "failed",
            "output": result.stdout,
            "error": result.stderr
        }
