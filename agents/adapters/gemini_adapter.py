"""
Gemini CLI Adapter
"""

import subprocess

class GeminiAdapter:
    def __init__(self, config):
        self.config = config

    def execute_task(self, task: dict) -> dict:
        command = [
            "gemini", "chat",
            "--prompt", task["description"],
            "--model", self.config.get("model", "gemini-2.0-flash")
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        return {
            "status": "success" if result.returncode == 0 else "failed",
            "output": result.stdout,
            "error": result.stderr
        }
