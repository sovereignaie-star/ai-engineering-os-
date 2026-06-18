"""
OpenCode Adapter
"""

import subprocess

class OpenCodeAdapter:
    def __init__(self, config):
        self.config = config

    def execute_task(self, task: dict) -> dict:
        command = ["opencode", "run", task["description"]]
        result = subprocess.run(command, capture_output=True, text=True)
        return {
            "status": "success" if result.returncode == 0 else "failed",
            "output": result.stdout,
            "error": result.stderr
        }
