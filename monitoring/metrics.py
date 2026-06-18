from dataclasses import dataclass
from typing import Dict, List
from datetime import datetime
import json

@dataclass
class AgentMetric:
    agent_name: str
    total_executions: int = 0
    successful_executions: int = 0
    failed_executions: int = 0
    total_duration: float = 0
    failures: List[Dict] = None

    def __post_init__(self):
        if self.failures is None:
            self.failures = []

class MetricsCollector:
    def __init__(self):
        self.metrics: Dict[str, AgentMetric] = {}

    def record_execution(self, agent_name: str, success: bool, duration: float, error: str = None):
        if agent_name not in self.metrics:
            self.metrics[agent_name] = AgentMetric(agent_name=agent_name)
        
        metric = self.metrics[agent_name]
        metric.total_executions += 1
        metric.total_duration += duration
        
        if success:
            metric.successful_executions += 1
        else:
            metric.failed_executions += 1
            if error:
                metric.failures.append({
                    "timestamp": datetime.now().isoformat(),
                    "error": error
                })

    def get_summary(self) -> dict:
        return {
            agent_name: {
                "total": metric.total_executions,
                "success": metric.successful_executions,
                "failed": metric.failed_executions,
                "avg_duration": metric.total_duration / metric.total_executions if metric.total_executions > 0 else 0,
                "failure_rate": metric.failed_executions / metric.total_executions if metric.total_executions > 0 else 0,
                "recent_failures": metric.failures[-5:]
            }
            for agent_name, metric in self.metrics.items()
        }
