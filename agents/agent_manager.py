"""
Agent Manager
يدير جميع الوكلاء ويوزع المهام عليهم
"""

from agents.adapters.openhands_adapter import OpenHandsAdapter
from agents.adapters.aider_adapter import AiderAdapter
from agents.adapters.swe_adapter import SWEAdapter
from agents.adapters.opencode_adapter import OpenCodeAdapter
from agents.adapters.plandex_adapter import PlandexAdapter
from agents.adapters.continue_adapter import ContinueAdapter
from agents.adapters.bolt_adapter import BoltAdapter
from agents.adapters.replit_adapter import ReplitAdapter
from agents.adapters.hermes_adapter import HermesAdapter
from agents.adapters.gemini_adapter import GeminiAdapter

class AgentManager:
    def __init__(self, config):
        self.config = config
        self.agents = {
            "openhands": OpenHandsAdapter(config),
            "aider": AiderAdapter(config),
            "swe": SWEAdapter(config),
            "opencode": OpenCodeAdapter(config),
            "plandex": PlandexAdapter(config),
            "continue": ContinueAdapter(config),
            "bolt": BoltAdapter(config),
            "replit": ReplitAdapter(config),
            "hermes": HermesAdapter(config),
            "gemini": GeminiAdapter(config),
        }

    def execute_task(self, agent_name: str, task: dict) -> dict:
        agent = self.agents.get(agent_name)
        if not agent:
            return {"status": "error", "message": f"Agent {agent_name} not found"}
        return agent.execute_task(task)

    def get_all_agents(self) -> list:
        return list(self.agents.keys())

    def get_agent_status(self, agent_name: str) -> dict:
        agent = self.agents.get(agent_name)
        if not agent:
            return {"status": "not_found"}
        return agent.get_status()
