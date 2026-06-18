import asyncio
from typing import Dict, List
from shared.contracts.agent_result import AgentResult
from agents.base_adapter import BaseAgentAdapter

class AgentManager:
    def __init__(self, config: dict):
        self.config = config
        self.agents: Dict[str, BaseAgentAdapter] = {}
        self.task_queue = asyncio.Queue()
        self.running_tasks = {}

    def register_agent(self, name: str, agent: BaseAgentAdapter):
        self.agents[name] = agent

    async def execute_task(self, agent_name: str, task: dict) -> AgentResult:
        import time
        start = time.time()
        
        agent = self.agents.get(agent_name)
        if not agent:
            return AgentResult(
                agent=agent_name,
                status="failed",
                stdout="",
                stderr=f"Agent {agent_name} not found",
                duration=0,
                error="Agent not found"
            )
        
        try:
            result = await agent.execute_task(task)
            duration = time.time() - start
            return AgentResult(
                agent=agent_name,
                status=result.get("status", "success"),
                stdout=result.get("output", ""),
                stderr=result.get("error", ""),
                duration=duration,
                files_changed=result.get("files_changed", []),
                error=result.get("error")
            )
        except Exception as e:
            return AgentResult(
                agent=agent_name,
                status="failed",
                stdout="",
                stderr=str(e),
                duration=time.time() - start,
                error=str(e)
            )

    def get_all_agents(self) -> List[str]:
        return list(self.agents.keys())
