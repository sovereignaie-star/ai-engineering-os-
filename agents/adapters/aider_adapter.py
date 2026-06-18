import subprocess
import asyncio
from agents.base_adapter import BaseAgentAdapter

class AiderAdapter(BaseAgentAdapter):
    def __init__(self, config):
        super().__init__(config)
        self.version = "0.86.2"
        self.agent_type = "cli"

    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        command = [
            "aider",
            "--message", task["description"],
            "--model", self.config.get("model", "gpt-4"),
            "--yes"
        ]
        
        process = await asyncio.create_subprocess_exec(
            *command,
            cwd=task.get("workspace", "."),
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
                "aider", "--version",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await process.communicate()
            return {"status": "healthy", "version": stdout.decode().strip()}
        except:
            return {"status": "unhealthy", "error": "aider not found"}

    async def stop_task(self, task_id: str) -> bool:
        return True
