from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime

class BaseAgentAdapter(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.agent_name = self.__class__.__name__.replace("Adapter", "").lower()

    @abstractmethod
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """تنفيذ مهمة معينة"""
        pass

    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """التحقق من صحة الوكيل"""
        return {"status": "healthy", "agent": self.agent_name}

    @abstractmethod
    async def stop_task(self, task_id: str) -> bool:
        """إيقاف مهمة قيد التنفيذ"""
        return True

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "name": self.agent_name,
            "version": getattr(self, "version", "1.0.0"),
            "type": getattr(self, "agent_type", "cli")
        }
