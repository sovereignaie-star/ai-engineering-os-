import subprocess
import asyncio
import os
from agents.base_adapter import BaseAgentAdapter

class OpenHandsAdapter(BaseAgentAdapter):
    def __init__(self, config):
        super().__init__(config)
        self.version = "0.47"
        self.agent_type = "docker"
        self.container_name = "ai-os-openhands"
        self.image = "ghcr.io/all-hands-ai/openhands:0.47"

    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
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
        
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        return {
            "status": "success" if process.returncode == 0 else "failed",
            "output": stdout.decode(),
            "error": stderr.decode(),
            "files_changed": [],
            "returncode": process.returncode
        }

    async def health_check(self) -> Dict[str, Any]:
        try:
            process = await asyncio.create_subprocess_exec(
                "docker", "images", "--format", "{{.Repository}}",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await process.communicate()
            if "openhands" in stdout.decode():
                return {"status": "healthy", "image": self.image}
            return {"status": "unhealthy", "error": "openhands image not found"}
        except:
            return {"status": "unhealthy", "error": "docker not available"}

    async def stop_task(self, task_id: str) -> bool:
        try:
            process = await asyncio.create_subprocess_exec(
                "docker", "stop", self.container_name,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
            return True
        except:
            return False
