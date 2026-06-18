"""
Replit Adapter
"""

import subprocess

class ReplitAdapter:
    def __init__(self, config):
        self.config = config

    def execute_task(self, task: dict) -> dict:
        command = ["replit", "run", "--project", task.get("project", ".")]
        result = subprocess.run(command, capture_output=True, text=True)
        return {
            "status": "success" if result.returncode == 0 else "failed",
            "output": result.stdout,
            "error": result.stderr
        }
