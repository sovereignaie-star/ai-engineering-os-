"""
OpenHands Adapter
يربط Orchestrator مع OpenHands عبر CLI
"""

import subprocess
import json
import os

class OpenHandsAdapter:
    def __init__(self, config):
        self.config = config
        self.container_name = "ai-os-openhands"
        self.image = "docker.all-hands.dev/all-hands-ai/openhands:0.47"

    def execute_task(self, task: dict) -> dict:
        command = [
            "docker", "run", "--rm",
            "--name", self.container_name,
            "-e", f"OPENAI_API_KEY={self.config.get('openai_api_key', '')}",
            "-v", f"{os.getcwd()}/workspaces:/workspace",
            "-v", "/var/run/docker.sock:/var/run/docker.sock",
            self.image,
            "python", "-m", "openhands.cli",
            "--task", task["description"]
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        return {
            "status": "success" if result.returncode == 0 else "failed",
            "output": result.stdout,
            "error": result.stderr
        }

    def get_status(self) -> dict:
        return {"status": "ready", "version": "0.47"}
