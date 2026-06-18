from agents.adapters import *

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

    def execute_task(self, agent_name, task):
        agent = self.agents.get(agent_name)
        if not agent:
            return {"status": "error", "message": f"Agent {agent_name} not found"}
        return agent.execute_task(task)

    def get_all_agents(self):
        return list(self.agents.keys())
