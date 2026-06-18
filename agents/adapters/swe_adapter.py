"""
SWE-agent Adapter
"""

import subprocess
import os

class SWEAdapter:
    def __init__(self, config):
        self.config = config
        self.image = "sweagent/swe-agent:latest"

    def execute_task(self, task: dict) -> dict:
        command = [
            "docker", "run", "--rm",
            "-v", f"{os.getcwd()}/workspaces:/workspace",
            "-e", f"OPENAI_API_KEY={self.config.get('openai_api_key', '')}",
            self.image,
            "--issue", task["description"]
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        return {
            "status": "success" if result.returncode == 0 else "failed",
            "output": result.stdout,
            "error": result.stderr
        }
